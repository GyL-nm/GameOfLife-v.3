    ### IMPORTS ###
import random as rdm

    ### Cell functions ###
# cell is set DEAD
def SetDead(grid, x,y): 
    """Set target cell as DEAD
    
    grid - main program grid
    
    x - horizontal position of cell
    
    y - vertical position of cell"""
    grid[y][x] = 0

# cell is set ALIVE
def SetAlive(grid, x,y): 
    """Set target cell as ALIVE
    
    grid - main program grid
    
    x - horizontal position of cell
    
    y - vertical position of cell"""
    grid[y][x] = 1

def ToggleCell(grid, x,y):
    """Toggles state of target cell
    
    grid - main program grid
    
    x - horizontal position of cell
    
    y - vertical position of cell"""
    if grid[y][x] == 0:
        grid[y][x] = 1
    else:
        grid[y][x] = 0

    ### Grid functions ###
# generate a blank grid with given dimensions
def GenerateGrid(x,y):
    """Generates an empty grid of specific dimensions
    
    x - horizontal size
    
    y - vertical size"""
    _grid = []  #temp grid
    for _y in range(y):
        _gridX = [] #temp grid row
        for _x in range(x):
            _gridX.append(0)
        _grid.append(_gridX) #assemble grid by appending rows
        
    return _grid

def NeighbourCheck(grid, x,y):
    """Evaluates 8 adjacent cells to a target cell to determine the cell's state next generation
    
    grid - main program grid
    
    x - horizontal position of cell
    
    y - vertical position of cell"""
    isAlive = grid[y][x]
    neighbourCount = 0
    TestPrint(f"\nCELL ({x},{y}) alive = {bool(isAlive)}") 
    for yOffset in range(-1,2):
        for xOffset in range(-1,2): #iterate over cells directly adjacent/diagonal from target cell
            _y = y+yOffset
            _x = x+xOffset
            if _y < 0 or _x < 0:
                TestPrint(f"({_x},{_y}) ignored")
                continue #ignore cells off the grid
            
            try:
                isNeighbourAlive = grid[_y][_x] #get state of target neighbour
                if isNeighbourAlive:
                    neighbourCount += 1
                    TestPrint(f"({x},{y}) neighbour ({_x},{_y}) ALIVE")
                    continue
                TestPrint(f"({x},{y}) neighbour ({_x},{_y}) DEAD")
            except IndexError:
                continue #ignore cells off the grid
    
    ######################################################################
    ###                   NEIGHBOUR CHECK RULES                        ###
    ### 1) All ALIVE cells with 2 or 3 ALIVE neighbours remain ALIVE.  ###
    ### 2) All DEAD cells with exactly 3 ALIVE neigbours become ALIVE. ###
    ### 3) All other cells are DEAD.                                   ###
    ######################################################################
    if isAlive:
        neighbourCount -= 1 #remove itself from neighbour count
        if neighbourCount == 2 or neighbourCount == 3:
            TestPrint(f"ALIVE cell ({x},{y}) ALIVE with {neighbourCount} neighbours")
            return 1 #ALIVE
        TestPrint(f"ALIVE cell ({x},{y}) DEAD with {neighbourCount} neighbours")
        return 0 #DEAD
    else:
        if neighbourCount == 3:
            TestPrint(f"DEAD cell ({x},{y}) ALIVE with {neighbourCount} neighbours")
            return 1 #ALIVE
        TestPrint(f"DEAD cell ({x},{y}) DEAD with {neighbourCount} neighbours")
        return 0 #DEAD

def UpdateGrid(grid):
    """Evaluates all cells in a grid via the NeighbourCheck method, iterating to a new generation
    
    grid - main program grid"""
    #only update if the new cell state for next generation is different from the current generation (for optimisation purposes)
    cellsToToggle = [] #list of cells that need to be changed
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            newCell = NeighbourCheck(grid, x,y) #evaluate neighbours of cell to get state next generation
            if newCell != grid[y][x]: #if cell next generation != current cell state
                cellsToToggle.append((x,y)) #add cell coordinates to list of cells to change

    for cell in cellsToToggle:
        ToggleCell(grid, cell[0],cell[1]) #toggle all cells that need to be changed

def RandomiseGrid(grid, chance):
    """Generates a grid with a random spread of DEAD and ALIVE cells
    
    grid - main program grid
    
    chance - random chance that a cell will spawn ALIVE (1/chance)"""
    _grid = grid  #temp grid
    x = len(_grid[0])
    y = len(_grid)
    for _y in range(y):
        for _x in range(x):
            if rdm.random() < 1/chance:
                _grid[_y][_x] = 1
            else:
                _grid[_y][_x] = 0
        
    grid = _grid

def Print2dArray(grid):
    """Prints a 2d Array in a readable format, with a coordinate axis border (FOR TESTING PURPOSES)
    
    grid - main program grid"""
    _grid = grid
    print("\n   ", end="")
    for x in range(len(_grid[0])):
        print(f"{x:2}", end=" ")
    print("")
    for y in range(len(_grid)):
        print(f"{y:3}", end=" ")
        for x in range(len(_grid[0])):
            if _grid[y][x] == 1:
                sym = "#"
            else:
                sym = " "
            print(f"{sym:3}", end="")
        print("")
    print("\n")

def TestPrint(str):
    global test
    if __name__ == "__main__":
        print(str)

# testing 
if __name__ == "__main__":
    
    while True:
        option = input("""Type:
[1] Generate Grid
[2] Randomise Grid
[3] Update Grid
[4] Toggle Cells
[5] Print Grid
[6] Print Grid Array
[7] QUIT
>> """)
        
        if option == "1":
            while True:
                try:
                    xInp = int(input("grid height >> "))
                    yInp = int(input("grid width >> "))
                    break
                except TypeError:
                    print("width/height must be a whole number")
            
            grid = GenerateGrid(xInp,yInp)
            Print2dArray(grid)
        
        elif option == "2":
            while True:
                try:
                    chance = int(input("Chance >> 1/"))
                    break
                except TypeError:
                    print("Chance must be a number")
            
            if grid == None:
                print("Grid must be created first, try Generate Grid")
                continue
                
            RandomiseGrid(grid, chance)
            Print2dArray(grid)
        
        elif option == "3":
            while True:
                try:
                    loop = int(input("Number of updates >> "))
                    pause = input("Pause between update (Y/N) >> ")
                    if pause.lower() == "y":
                        pause = True
                    elif pause.lower() == "n":
                        pause = False
                    else:
                        raise TypeError
                    
                    break
                except TypeError:
                    print("Invalid option")
                     
            if grid == None:
                print("Grid must be created first, try Generate Grid")
                continue
            
            for i in range(loop):
                UpdateGrid(grid)
                Print2dArray(grid)
                print(f"LOOP{i+1} COMPLETE")
                if pause:
                    input("PAUSE")
        
        elif option == "4":
            quit = ""
            while quit != "q":
                while True:
                    try:
                        xInp = int(input("x >> "))
                        yInp = int(input("y >> "))
                        break
                    except TypeError or IndexError:
                        print("Must be a whole number")
                        
                if grid == None:
                    print("Grid must be created first, try Generate Grid")
                    continue
            
                ToggleCell(grid, xInp,yInp)
                Print2dArray(grid)
                quit = input("'q' to stop >> ")
            
            
            
            
                
        elif option == "5":
            
            if grid == None:
                print("Grid must be created first, try Generate Grid")
                continue
            
            Print2dArray(grid)

        elif option == "6":
            
            if grid == None:
                print("Grid must be created first, try Generate Grid")
                continue
            
            print(grid)
        
        elif option == "7":
            break
        
        else:
            print("Please choose an option")
            continue
    
else:
    print("*** grid module successfully loaded ***")
