from guizero import App, Window, Box, Text, PushButton, TextBox, Slider, Waffle, MenuBar, Combo, CheckBox
from pathlib import Path
import math

import grid

test = False
mainGrid = grid.GenerateGrid(25,25)

def Display():
    app.display()

def TogglePixel(_grid, x,y, color):
    grid.ToggleCell(_grid, x,y)
    if gameGridWfl[x,y].color == "black":
        gameGridWfl.set_pixel(x, y, color) 
    else:
        gameGridWfl.set_pixel(x, y, "black") 

def GenerateGrid(_grid, height, width):
    grid.GenerateGrid(width,height)
    
    #resize grid
    gameGridWfl.height = height
    gameGridWfl.width = width
    
    xSld.value = width
    ySld.value = height
    gameGridWfl.show()
    
    for y in range(len(_grid)):
        for x in range(len(_grid[0])):
            if gameGridWfl[x,y].color != "black":
                gameGridWfl[x,y].color = "black"

def UItoGrid(_grid):
    newGrid = []
    for y in range(gameGridWfl.height):
        for x in range(gameGridWfl.width):
            if gameGridWfl[x,y].color != "black":
                newGrid.append(1)
            else:
                newGrid.append(0)
    _grid = newGrid

def UpdateGrid(_grid, height, width):
    UItoGrid(_grid)
    grid.UpdateGrid(_grid)
    #ResizeWindow()
    
    #resize grid
    xSld.value = width
    ySld.value = height
    #SetPixelSize()
    gameGridWfl.height = height
    gameGridWfl.width = width
    #PixelSize(gridX, gridY)
    #make sure grid is visible
    gameGridWfl.show()
    
    for y in range(len(_grid)):
        for x in range(len(_grid[0])):
            if gameGridWfl[x,y].color != "black":
                cell = 1 #ALIVE
            else:
                cell = 0 #DEAD

            #only update if the new cell state for next tick is different from the current tick (for optimisation purposes)
            if cell != _grid[y][x]:
                TogglePixel(_grid, x,y, CellColor(x,y))

def GenerateGridCall():
    UpdateGrid(mainGrid, ySld.value, xSld.value)
    
def UpdateGridCall():
    UpdateGrid(mainGrid, ySld.value, xSld.value)
    
def LoadSeed():
    pass

def SaveSeed():
    pass

def LoadPattern():
    pass

def SavePattern():
    pass

def RecolorGrid():
    for y in range(gameGridWfl.height):
        for x in range(gameGridWfl.width):
            if gameGridWfl[x,y].color != "black":
                gameGridWfl[x,y].color = CellColor(x,y)

def ColorMode0():
    global colorMode
    colorMode = 0
    RecolorGrid()

def ColorMode1():
    global colorMode
    colorMode = 1
    ColorPopup()
    CustomColor()

def ColorMode2():
    global colorMode
    colorMode = 2
    RecolorGrid()

colorMode = 0
customColor = (255,255,255)
def CellColor(x,y):
    global colorMode
    if colorMode == 0:
        color = (255,255,255)
    elif colorMode == 1:
        color = customColor
    elif colorMode == 2:
        colorX = max(0, min(255, x*(round(255/gameGridWfl.width))))
        colorY = max(0, min(255, y*(round(255/gameGridWfl.height))))
        avg = max(0, min(255, round((colorX+colorY/2))))
        color = (colorX, colorY, 255-avg)
    
    return color

def CustomColor():
    global customColor
    customColor = (colorRSld.value,colorGSld.value,colorBSld.value)
    colorBox.bg = customColor
    RecolorGrid()

def WaffleClick(x,y):
    TogglePixel(mainGrid, x,y, CellColor(x,y))

def GuidePopup():
    tutorialWn.show()

def ColorPopup():
    colorWn.show()
    
### MAIN WINDOW ###
app = App(title="Conway's Game of Life - Generation 0")
menuBar = MenuBar(app,
                toplevel=["File", "Pattern", "Colour"], 
                options=[
                    [ ["Load Seed", LoadSeed], ["Save Seed", SaveSeed] ], 
                    [ ["Import Pattern", LoadPattern], ["Export Pattern", SavePattern] ],
                    [ ["Black/White",ColorMode0],["Custom",ColorMode1],["XY gradient",ColorMode2] ]
                ])

UIBox = Box(app, 
            align="top", 
            layout="grid")
UIBox.bg = "grey"

waffleBox = Box(UIBox, 
                layout="grid", 
                grid=[1,0], 
                height="fill",
                width="fill")

genCountT = Text(waffleBox, 
                 grid=[0,0], 
                 text="Generation 0")

gameGridWfl = Waffle(waffleBox, 
                     grid=[0,1], 
                     height=25, 
                     width=25, 
                     pad=0.1, 
                     dim=15, 
                     color="black", 
                     command=WaffleClick)

parameterBox = Box(UIBox, 
                   grid=[0,0], 
                   align="left")
parameterBox.bg = "light grey"

sliderBox = Box(parameterBox, 
                layout="grid")

xSld = Slider(waffleBox, 
              grid=[0,2], 
              start=3, 
              end=250, 
              height=5)

ySld = Slider(waffleBox, 
              grid=[1,1], 
              start=3, 
              end=250, 
              width=5, 
              horizontal=False)
xSld.value = gameGridWfl.width
ySld.value = gameGridWfl.height

PButtonBox = Box(parameterBox, layout="grid")

generatePB = PushButton(PButtonBox, grid=[0,0], width=15, text="Generate Grid", command=GenerateGridCall)


advancePB = PushButton(parameterBox, grid=[0,1],width=34, text="Advance Generation", command=UpdateGridCall)

### COLOUR PICKER ###
colorWn = Window(app,
                 title="Custom Colour",
                 visible=False,
                 height=200,
                 width=300)
colorWnBox = Box(colorWn,
                 layout="grid",
                 align="top")

colorBox = Box(colorWnBox,
               grid=[1,0],
               height=50,
               width=50,
               border=2)

colorRT = Text(colorWnBox,
               text="R",
               grid=[0,1])
colorRSld = Slider(colorWnBox,
                   start=0,
                   end=255,
                   grid=[1,1],
                   height=2,
                   command=CustomColor)

colorGT = Text(colorWnBox,
               text="G",
               grid=[0,2])
colorGSld = Slider(colorWnBox,
                   start=0,
                   end=255,
                   grid=[1,2],
                   height=2,
                   command=CustomColor)

colorBT = Text(colorWnBox,
               text="B",
               grid=[0,3])
colorBSld = Slider(colorWnBox,
                   start=0,
                   end=255,
                   grid=[1,3],
                   height=2,
                   command=CustomColor)

### TUTORIAL WINDOW ###
tutorialWn = Window(app, 
                    title="Tutorial", 
                    visible=False)

Display()


if test:
    testGrid = grid.GenerateGrid(10,10)
    grid.Print2dArray(testGrid)