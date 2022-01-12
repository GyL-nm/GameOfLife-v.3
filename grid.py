    ### IMPORTS ###
from random import randint as randi

    ### Cell functions ###
# cell is set DEAD
def SetDead(grid, x,y): 
    grid[y][x] = 0

# cell is set ALIVE
def SetAlive(grid, x,y): 
    grid[y][x] = 1

def ToggleCell(grid, x,y):
    if grid[y][x] == 0:
        grid[y][x] = 1
    else:
        grid[y][x] = 0

    ### Grid functions ###
# generate a blank grid with given dimensions
def GenerateGrid(x,y):
    """Generates an empty grid
    
    x - horizontal dimension size\n
    y - vertical dimension size"""
    _grid = []  #temp grid
    for _y in range(y):
        _gridX = [] #temp grid row
        for _x in range(x):
            _gridX.append(0)
        _grid.append(_gridX) #assemble grid by appending rows
        
    return _grid

def RandomiseGrid(grid):
    _grid = grid  #temp grid
    x = len(_grid[0])
    y = len(_grid)
    for _y in range(y):
        for _x in range(x):
            _grid[_y][_x] = randi(0,1)
        
    grid = _grid

def NeighbourCheck(grid, x,y):
    #print(grid[y][x])
    isAlive = grid[y][x]
    neighbourCount = 0
    #print(f"\nCELL ({x},{y})")
    #print(f"({x},{y}) alive = {isAlive}")
    for yOffset in range(-1,2):
        for xOffset in range(-1,2):
            _y = y+yOffset
            _x = x+xOffset
            if _y < 0 or _x < 0:
                #print(f"({_x},{_y}) ignored")
                continue
            
            try:
                isNeighbourAlive = grid[_y][_x]
                if isNeighbourAlive:
                    neighbourCount += 1
                    #print(f"({x},{y}) neighbour ({_x},{_y}) ALIVE")
                    continue
                #print(f"({x},{y}) neighbour ({_x},{_y}) DEAD")
            except IndexError:
                continue
            
    if isAlive:
        neighbourCount -= 1
        if neighbourCount == 2 or neighbourCount == 3:
            #print(f"ALIVE cell ({x},{y}) ALIVE with {neighbourCount} neighbours")
            return 1 #ALIVE
        #print(f"ALIVE cell ({x},{y}) DEAD with {neighbourCount} neighbours")
        return 0 #DEAD
    else:
        if neighbourCount == 3:
            #print(f"DEAD cell ({x},{y}) ALIVE with {neighbourCount} neighbours")
            return 1 #ALIVE
        #print(f"DEAD cell ({x},{y}) DEAD with {neighbourCount} neighbours")
        return 0 #DEAD

def UpdateGrid(grid):
    cellsToToggle = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            newCell = NeighbourCheck(grid, x,y)
            if newCell != grid[y][x]:
                cellsToToggle.append((x,y))

    for cell in cellsToToggle:
        ToggleCell(grid, cell[0],cell[1])

            
            

def NeighbourCheck2(grid):
    pass

def Print2dArray(grid):
    _grid = grid
    print("   ", end="")
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


# for testing
if __name__ == "__main__":
    #yInp = int(input("grid width >> "))
    #xInp = int(input("grid height >> "))

    testGrid = [   [0,0,0,0,0],
                    [0,0,1,0,0],
                    [0,1,1,1,0],
                    [0,0,1,0,0],
                    [0,0,0,0,0] ]
    Print2dArray(testGrid)
    for i in range(2):
        UpdateGrid(testGrid)
        Print2dArray(testGrid)
else:
    print("*** grid module successfully loaded ***")