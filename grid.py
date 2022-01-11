    ### IMPORTS ###
from random import randint as randi

    ### Cell functions ###
# cell is set DEAD
def SetDead(grid, x,y): 
    grid[y][x] = 0

# cell is set ALIVE
def SetAlive(grid, x,y): 
    grid[y][x] = 1

# check if cell is ALIVE
def IsAlive(cell):   
    if cell == 1:
        return True 
    return False

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
    _grid = grid
    alive = IsAlive(_grid[y][x])
    neighbourCount = 0
    print(f"\nCELL ({x},{y})")
    for yOffset in range(-1,2):
        for xOffset in range(-1,2):
            _y = y+yOffset
            _x = x+xOffset
            if _y < 0 or _x < 0 or _y >= len(_grid) or _x >= len(_grid[0]) or (x,y) == (_x,_y):
                print(f"({_x},{_y}) ignored")
                continue
            
            checkCell = _grid[_y][_x]
            if IsAlive(checkCell):
                neighbourCount += 1
                print(f"({x},{y}) neighbour ({_x},{_y}) ALIVE")
                continue
            print(f"({x},{y}) neighbour ({_x},{_y}) DEAD")
    
    if alive:
        if neighbourCount == 2 or neighbourCount == 3:
            print(f"ALIVE cell ({x},{y}) ALIVE with {neighbourCount} neighbours")
            return 1 #ALIVE
        print(f"ALIVE cell ({x},{y}) DEAD with {neighbourCount} neighbours")
        return 0 #DEAD
    else:
        if neighbourCount == 3:
            print(f"DEAD cell ({x},{y}) ALIVE with {neighbourCount} neighbours")
            return 1 #ALIVE
        print(f"DEAD cell ({x},{y}) DEAD with {neighbourCount} neighbours")
        return 0 #DEAD
        

def UpdateGrid(grid):
    _grid = grid #temp grid
    _newGrid = grid
    for y in range(len(_grid)):
        for x in range(len(_grid[0])):
            oldCell = _grid[y][x]
            _newGrid[y][x] = oldCell
            newCell = NeighbourCheck(grid, x,y)
            if newCell != oldCell:
                _newGrid[y][x] = newCell
    
    grid = _newGrid
            
            
            

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
    
    testGrid1 = GenerateGrid(10, 10)
    Print2dArray(testGrid1)
    RandomiseGrid(testGrid1)
    Print2dArray(testGrid1)
    for i in range(5):
        UpdateGrid(testGrid1)
        Print2dArray(testGrid1)
    
    testGrid2 = GenerateGrid(10, 10)
    testGrid2[3][3] = 1
    testGrid2[4][2] = 1 
    testGrid2[4][3] = 1
    testGrid2[4][4] = 1
    testGrid2[5][3] = 1
    Print2dArray(testGrid2)
    for i in range(10):
        UpdateGrid(testGrid2)
        Print2dArray(testGrid2)
else:
    print("*** grid module successfully loaded ***")