import tkinter
from guizero import App, Window, Box, Text, PushButton, TextBox, Slider, Waffle, MenuBar, Combo, CheckBox
from pathlib import Path
import math
import random as rdm

import grid

test = False 
mainGrid = grid.GenerateGrid(25,25)

def display():
    app.display()

def TogglePixel(uiGrid, x,y, color):
    """Toggles a target pixel on the UI grid
    
    uiGrid - UI grid object
    
    x - horizontal position of cell
    
    y - vertical position of cell
    
    color - RGB value for ALIVE cell"""
    if uiGrid[x,y].color == "black": #If cell !DEAD
        uiGrid.set_pixel(x, y, color) #Toggle DEAD cell to ALIVE
    else:
        uiGrid.set_pixel(x, y, "black") #Else toggle ALIVE cell to DEAD

def UItoGrid(_grid, uiGrid):
    """Converts UI grid cell colour data into a 2D array of 1s and 0s for ALIVE and DEAD cells
    
    _grid - main program grid
    
    uiGrid - UI grid object"""
    newGrid = [] #temp grid
    for y in range(uiGrid.height):
        newRow = [] #temp grid row
        for x in range(uiGrid.width):
            if gameGridWfl[x,y].color != "black": #If cell !Dead
                newRow.append(1) #Add ALIVE cell to temp row
            else:
                newRow.append(0) #Else add DEAD cell to temp row
        newGrid.append(newRow) #Add row to temp grid
    
    return newGrid

def ResizeGrid(uiGrid, height, width):
    """Resizes grid dimension in pixels and updates slider values
    
    uiGrid - UI grid object
    
    height - vertical grid dimensions
    
    width - horizontal grid dimensions"""
    gameGridWfl.height = height #Set UI grid height in pixels
    gameGridWfl.width = width #Set UI grid width in pixels
    
    ySld.value = height #Update y slider to show new height
    xSld.value = width #Update x slider to show new width
    
    gameGridWfl.show() #Make sure grid is updated

def GenerateGrid(_grid, uiGrid, height, width):
    """Generates an empty grid of specific dimensions
    
    _grid - main program grid
    
    uiGrid - UI grid object
    
    height - horizontal size
    
    height - vertical size"""
    ResizeGrid(uiGrid, height, width) #Make sure grid dimensions are consistent between the UI and main program grid
    
    _grid = UItoGrid(_grid, uiGrid) #Convert UI grid into 2D array
    grid.GenerateGrid(width,height) #Generate new grid 
    
    for y in range(len(_grid)):
        for x in range(len(_grid[0])):
            #only update if the new cell state for next generation is different from the current generation (for optimisation purposes)
            if uiGrid[x,y].color != "black": #If cell !DEAD
                uiGrid[x,y].color = "black" #Set ALIVE cell to DEAD

def UpdateGrid(_grid, uiGrid, height, width):
    """Updates the grid to the next generation
    
    _grid - main program grid
    
    uiGrid - UI grid object
    
    height - horizontal size
    
    height - vertical size"""
    ResizeGrid(uiGrid, height, width) #Make sure grid dimensions are consistent between the UI and main program grid
    
    _grid = UItoGrid(_grid, uiGrid) #Convert UI grid into 2D array
    grid.UpdateGrid(_grid) #Evaluate all cells to determine their state next generation
    
    for y in range(height):
        for x in range(width):
            if uiGrid[x,y].color != "black": #If cell !DEAD
                cell = 1 #flag as ALIVE
            else:
                cell = 0 #flag as DEAD

            #only update if the new cell state for next generation is different from the current generation (for optimisation purposes)
            if cell != _grid[y][x]:
                TogglePixel(uiGrid, x,y, CellColor(x,y)) #Toggle cell

def RandomiseGrid(_grid, uiGrid, height, width, chance):
    """Generates a grid with a random spread of DEAD and ALIVE cells
    
    _grid - main program grid
    
    uiGrid - UI grid object
    
    height - horizontal size
    
    height - vertical size
    
    chance - random chance that a cell will spawn ALIVE (1/chance)"""
    ResizeGrid(uiGrid, height, width) #Make sure grid dimensions are consistent between the UI and main program grid
    
    _grid = UItoGrid(_grid, uiGrid) #Convert UI grid into 2D array
    grid.RandomiseGrid(_grid, chance) #Randomise all cells in the grid based on chance parameter
    
    for y in range(height):
        for x in range(width):
            if uiGrid[x,y].color != "black":
                cell = 1 #flag as ALIVE
            else:
                cell = 0 #flag as DEAD

            #only update if the new cell state for next generation is different from the current generation (for optimisation purposes)
            if cell != _grid[y][x]:
                TogglePixel(uiGrid, x,y, CellColor(x,y)) #Toggle cell
    
def LoadSeed():
    pass

def SaveSeed():
    pass

def LoadPattern():
    pass

def SavePattern():
    pass


def RecolorGrid(uiGrid):
    """Update colour of all cells in the UI grid to match colour mode set by user
    
    uiGrid - UI grid object"""
    for y in range(uiGrid.height):
        for x in range(uiGrid.width):
            if uiGrid[x,y].color != "black":
                uiGrid[x,y].color = CellColor(x,y)

colorMode = 0
customColor = (255,255,255)
def CellColor(x,y):
    """Determine the colour of a given cell based on its coordinates and colour mode set by user
    
    x - horizontal position of cell
    
    y - vertical position of cell"""
    global colorMode
    if colorMode == 0: #Black and white
        color = (255,255,255) 
    elif colorMode == 1: #Custom colour (through RGB colour picker settings)
        color = customColor
    elif colorMode == 2: #RGBY gradient based on coordinates of cells in the grid
        colorX = max(0, min(255, x*(round(255/gameGridWfl.width))))
        colorY = max(0, min(255, y*(round(255/gameGridWfl.height))))
        avg = max(0, min(255, round((colorX+colorY/2))))
        color = (colorX, colorY, 255-avg)
    
    return color

def CustomColor():
    """Update customColor when RGB sliders are changed"""
    global customColor
    customColor = (colorRSld.value,colorGSld.value,colorBSld.value) #get RGB values from sliders
    colorBox.bg = customColor #Display colour in colour picker window
    RecolorGrid(gameGridWfl) #Update UI grid colours in realtime

def ColorMode0():
    """Set colorMode to 0 (Black and white)"""
    global colorMode
    colorMode = 0
    RecolorGrid(gameGridWfl) #Update UI grid colours in realtime

def ColorMode1():
    """Set colorMode to 1 (Custom colour)"""
    global colorMode
    colorMode = 1
    ColorPopup()
    CustomColor(gameGridWfl) #Update UI grid colours in realtime

def ColorMode2():
    """Set colorMode to 0 (XY Gradient)"""
    global colorMode
    colorMode = 2
    RecolorGrid(gameGridWfl) #Update UI grid colours in realtime

def WaffleClick(x,y):
    """Toggle cells when clicked on the UI grid"""
    TogglePixel(gameGridWfl, x,y, CellColor(x,y))

def GenerateGridCall():
    """Call GenerateGrid when generatePB button is pressed"""
    GenerateGrid(mainGrid, gameGridWfl, ySld.value, xSld.value)
    
def UpdateGridCall():
    """Call UpdateGrid when advancePB button is pressed"""
    UpdateGrid(mainGrid, gameGridWfl, gameGridWfl.height, gameGridWfl.width)
    
def RandomiseGridCall():
    """Call RandomiseGrid when randomisePB button is pressed"""
    RandomiseGrid(mainGrid, gameGridWfl, gameGridWfl.height, gameGridWfl.width, optionsRandomPageOption1Sld.value)

def OptionsPopup():
    """Open optionsWn window when pressed in the MenuBar"""
    optionsWn.show()
    optionsWn.focus()

def OptionsPage(page):
    """Change pages in the options menu
    
    page - target option page"""
    global optionsPages
    global optionsPageButtons
    
    for p in optionsPages:
        p.hide() #Hide all pages
        p.bg = "light gray" #De-highlight all page buttons
        
    optionsPages[page].show() #Hide target page
    optionsPageButtons[page].bg = "gray" #Highlight target page button

def ColorPopup():
    """Open colorWn window when pressed in the MenuBar"""
    colorWn.show()
    colorWn.focus()
    
# def TutorialPopup():
#     tutorialWn.show()

def Highlight(eventData):
    """Highlight a button on any event
    
    eventData - data from the widget"""
    eventData.widget.bg = (220,220,220)

def Lowlight(eventData):
    """De-highlight a button on any event
    
    eventData - data from the widget"""
    eventData.widget.bg = (255,255,255)

### MAIN WINDOW ###
app = App(title="Conway's Game of Life - Generation 0")
app.bg = "light gray"
app.font = "helvetica"

menuBar = MenuBar(app,
                toplevel=["File", "Pattern", "Colour"], 
                options=[
                    [ ["Options", OptionsPopup], ["Load Seed", LoadSeed], ["Save Seed", SaveSeed] ], 
                    [ ["Import Pattern", LoadPattern], ["Export Pattern", SavePattern] ],
                    [ ["Black/White",ColorMode0],["Custom",ColorMode1],["XY Gradient",ColorMode2] ]
                ])

UIPadBox = Box(app, align="top")
UIPadBox.set_border(50,"light gray")

UIBox = Box(UIPadBox, 
            align="top", 
            layout="grid",
            border=2)
UIBox.bg = "gray"
UIBox.set_border(3,(150,150,150))

    # Game Grid #
waffleBox = Box(UIBox, 
                layout="grid", 
                grid=[1,0], 
                height="fill",
                width="fill")
UIPadBox.set_border(10,"light gray")

# genCountT = Text(waffleBox, 
#                  grid=[0,0], 
#                  text="Generation 0")

gameGridWfl = Waffle(waffleBox, 
                     grid=[0,1], 
                     height=25, 
                     width=25, 
                     pad=0.1, 
                     dim=15, 
                     color="black", 
                     command=WaffleClick)

    # Controls #
parameterBox = Box(UIBox, 
                   grid=[0,0], 
                   align="left")
parameterBox.bg = "grey"
parameterBox.set_border(10,"gray")

        # Grid Sliders #
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

        # Push Buttons #
PButtonBox = Box(parameterBox, 
                 layout="grid")
PButtonBox.bg = "gray"


generatePB = PushButton(PButtonBox, 
                        grid=[0,0], 
                        width=15,
                        height=2, 
                        text="Generate Grid", 
                        command=GenerateGridCall)
randomisePB = PushButton(PButtonBox, 
                        grid=[1,0], 
                        width=15,
                        height=2, 
                        text="Randomise Grid", 
                        command=RandomiseGridCall)

advancePB = PushButton(parameterBox, grid=[0,2],
                       width=34,
                       height=2,
                       text="Advance Generation", 
                       command=UpdateGridCall)

generatePB.bg = "white"
generatePB.when_mouse_enters = Highlight
generatePB.when_mouse_leaves = Lowlight

advancePB.bg = "white"
advancePB.when_mouse_enters = Highlight
advancePB.when_mouse_leaves = Lowlight

randomisePB.bg = "white"
randomisePB.when_mouse_enters = Highlight
randomisePB.when_mouse_leaves = Lowlight

### OPTIONS ###
optionsWn = Window(app,
                   title="Options",
                   visible=False,
                   height=300,
                   width=735)
optionsWn.bg = "gray"
optionsWn.font = "helvetica"


optionsTopbarBox = Box(optionsWn,
                       layout="grid",
                       align="top",
                       width="fill")
optionsTopbarBox.bg = "light gray"
optionsTopbarBox.set_border(2,(150,150,150))

    # Random Options Page #
optionsTopbarRandomPB = PushButton(optionsTopbarBox,
                                   text="Random",
                                   align="left",
                                   grid=[0,0],
                                   height=1,
                                   width=15,
                                   command=OptionsPage,
                                   args=[0])
optionsTopbarRandomPB.bg = "gray"
optionsTopbarRandomPB.text_size = 8

optionsRandomPageBox = Box(optionsWn,
                           layout="grid")
optionsRandomPageBox.bg = "light gray"
optionsRandomPageBox.set_border(5,(150,150,150))

optionsRandomPageColumn0T = Text(optionsRandomPageBox,
                                 grid=[0,1],
                                 text="Option",
                                 font="helvetica",
                                 size=7)

optionsRandomPageColumn0T = Text(optionsRandomPageBox,
                                 grid=[2,1],
                                 text="Description",
                                 font="helvetica",
                                 size=7)

optionsRandomPageOption1T = Text(optionsRandomPageBox,
                                 grid=[0,2],
                                 text="Random Chance",
                                 font="helvetica",
                                 size=8)

optionsRandomPageOption1Sld = Slider(optionsRandomPageBox,
                                 grid=[1,2],
                                 height=2,
                                 start=1,
                                 end=50)
optionsRandomPageOption1Sld.value = 3

optionsRandomPageDesc1T = Text(optionsRandomPageBox,
                                 grid=[2,2],
                                 text="The chance that a cell will spawn as ALIVE when the grid is randomised",
                                 font="helvetica",
                                 size=8)


optionsPages = [optionsRandomPageBox]
optionsPageButtons = [optionsTopbarRandomPB]

### COLOUR PICKER ###
colorWn = Window(app,
                 title="Custom Colour",
                 visible=False,
                 height=200,
                 width=300)
colorWn.font = "helvetica"

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

colorRSld.value = 255
colorGSld.value = 255
colorBSld.value = 255

### TUTORIAL WINDOW ###
# tutorialPB = PushButton(app,
#                         text="Tutorial",
#                         align="bottom",
#                         width=15,
#                         command=TutorialPopup)
# tutorialPB.bg = "white"
# tutorialPB.when_mouse_enters = Highlight
# tutorialPB.when_mouse_leaves = Lowlight

# tutorialWn = Window(app, 
#                     title="Tutorial", 
#                     visible=False)
# tutorialWn.font = "helvetica"

if test:
    testGrid = grid.GenerateGrid(10,10)
    grid.Print2dArray(testGrid)
    grid.RandomiseGrid(testGrid)
    grid.Print2dArray(testGrid)
    UpdateGrid(testGrid)

display()





    