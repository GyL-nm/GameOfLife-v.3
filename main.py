from guizero import App, Window, Box, Text, PushButton, TextBox, Slider, Waffle, MenuBar, Combo, CheckBox
from pathlib import Path

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
                
    global genCount
    genCount = 0
    app.title = "Conway's Game of Life - Generation 0"

def SetGrid(_grid, newGrid, uiGrid, height, width):
    """Generates an new grid with a given arrangement
    
    _grid - main program grid
    
    newGrid - new grid arrangement to be grafted onto _grid
    
    uiGrid - UI grid object
    
    height - horizontal size
    
    height - vertical size"""
    ResizeGrid(uiGrid, height, width) #Make sure grid dimensions are consistent between the UI and main program grid
    
    _grid = newGrid
    
    for y in range(height):
        for x in range(width):
            if uiGrid[x,y].color != "black": #If cell !DEAD
                cell = 1 #flag as ALIVE
            else:
                cell = 0 #flag as DEAD

            #only update if the new cell state for next generation is different from the current generation (for optimisation purposes)
            if cell != _grid[y][x]:
                TogglePixel(uiGrid, x,y, CellColor(x,y)) #Toggle cell
    
    global genCount
    genCount = 0
    app.title = "Conway's Game of Life - Generation 0"

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
    
    global genCount
    
    genCount += 1
    app.title = f"Conway's Game of Life - Generation {genCount}"

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
    
    global genCount
    genCount = 0
    app.title = "Conway's Game of Life - Generation 0"

def CreatePatternAuto(_grid):
    # combine to make a bounding box around pattern
    x1 = len(_grid[0]) # x of pixel closest to the y axis
    x2 = 0 # x of pixel furthest from the y axis
    y1 = None # y of first ALIVE pixel
    y2  = None # y of last ALIVE pixel
    
    #loop over all grid pixels
    for y in range(len(_grid)):
        for x in range(len(_grid[0])):
            #if pixel is ALIVE
            if _grid[y][x] == 1:
                #hold as last pixel
                y2 = y
                #check for first ALIVE pixel
                if y1 == None:
                    y1 = y

                #check if current pixel is closer to y axis than the current closest (left-most pixel)
                if x < x1:
                    x1 = x
                #check if current pixel is further from the y axis than the current furthest (right-most pixel)
                elif x > x2:
                    x2 = x
        
    coords = [x1,y1,x2,y2]
    if None in coords:
        #error message
        app.error("Invalid pattern", "There is no pattern to create as the canvas is blank.")
        return False
    
    pattern = []
    #create mini-grid of pixels from bounding box data
    for y in range(y1, y2+1):
        patternY = []
        for x in range(x1, x2+1):
            patternY.append(_grid[y][x])
        pattern.append(patternY)
    
    return pattern

clipboard = []
def CreatePatternManual(_grid, x1,y1, x2,y2):
    global clipboard
    
    coords = [x1,y1,x2,y2]
    if None in coords:
        #error message
        app.error("Invalid pattern", "The bounding box was not placed properly.")
        return False

    pattern = []
    for y in range(y1, y2+1):
        patternY = []
        for x in range(x1, x2+1):
            patternY.append(_grid[y][x])
        pattern.append(patternY)
        
    clipboard.append(pattern)
    return pattern

def LoadSeed(_grid, uiGrid):
    folderPath = str(Path(__file__).parent.absolute()) + "/seeds" # get path to "seeds" subfolder
    
    try:
        filepath = app.select_file(folder=folderPath, filetypes=[ ["Hex Seed (*.seed)", ".seed"] ]) # windows dialogue popup for accessing files
    except FileNotFoundError:
        app.error("No file found", "No file was found.") # error popup when no file is selected
        return
        
    with open(filepath,"r") as file:
        seed = file.read() # read seed data from .seed file (last 6 characters are the dimensions needed to add leading zeros to the binary seed e.g "01A5E0|020012")
    seedH = seed[:-6] # take hex data for seed
        
    dim = seed[-6:] # take last 6 characters for grid dimensions
    dimX = int(dim[3:]) # split dimensions into x and y
    dimY = int(dim[:3])
    
    seedBLength = dimX*dimY # get length of flattened 2D array
    seedB = (bin(int(seedH, 16))[2:]).zfill(seedBLength) # add leading zeros to the binary seed
    
    loadGrid = []
    for y in range(dimY): # reformat the flattened list into a 2D array using dimensions data
        loadGridX = []
        for x in range(dimX):
            loadGridX.append(int(seedB[(y*dimX)+x]))
        loadGrid.append(loadGridX)
        print(loadGridX)
    
    SetGrid(_grid, loadGrid, uiGrid, dimY,dimX) # parse loaded grid onto mainGrid
    
def SaveSeed(_grid, uiGrid):
    folderPath = str(Path(__file__).parent.absolute()) + "/seeds" # get path to "seeds" subfolder
    
    try:
        filepath = app.select_file(save=True, folder=folderPath, filetypes=[ ["Hex Seeds (*.seed)", ".seed"] ]) + ".seed" # windows dialogue popup for saving files
    except FileNotFoundError:
        app.error("Invalid filepath", "A valid filepath must be selected to save this file.") # error popup when no file is created
        return
    
    filename = (Path(filepath).name).replace(".seed","")
    if filename.rstrip() == "":
        app.error("Invalid filepath", "A valid filename must be entered to save this file.") # error popup when file has no name
        return
    
    _grid = UItoGrid(_grid, uiGrid) # copy the current UI grid to the mainGrid for continuity
    
    seedB = ""
    for row in _grid:
        for cell in row:
            seedB += str(cell) # flatten 2D grid into list
    
    seedH = hex(int(seedB, 2)) # convert binary seed into hex (removes leading zeros)
    dimStr = str(len(mainGrid)).zfill(3) + str(len(mainGrid[0])).zfill(3) # create 6 character string to store the grid dimensions
    
    seed = seedH + dimStr # add dimension data to end of the seed
    
    with open(filepath,"x") as file:
        file.write(seed) # write seed to file

patternDict = {}
def LoadPattern(_grid, uiGrid):
    global patternDict
    folderPath = str(Path(__file__).parent.absolute()) + "\patterns" # get path to "patterns" subfolder
    
    try:
        filepath = app.select_file(folder=folderPath, filetypes=[ ["2D Patterns (*.pattern)", ".pattern"] ]) # windows dialogue popup for accessing files
    except FileNotFoundError:
        app.error("No file found", "No file was found.") # error popup when no file is found
        return
    
    filename = (Path(filepath).name).replace(".pattern","") # remove file extension to get filename string
    
    
    if filename.rstrip() == "":
        app.error("No file found", "No file was found.") # error popup when invalid filename is used
        return
    
    with open(filepath,"r") as file:
        try:
            pattern = eval(file.read()) # convert string into 2D array
        except SyntaxError:
            app.error("Unrecognisable file", "The file could not be read or was formatted incorrectly.") # error popup when the array string is formatted incorrectly
            return
    
    patternDict[filename] = pattern # add the pattern to the dictionary
    
    fileLines = [] 
    for key in patternDict:
            fileLines.append((str(key) + ";" + str(patternDict[key]) + "\n")) # new line for each pattern
    fileLines[-1] = fileLines[-1].replace("\n","") # remove newline from last line to prevent empty pattern entries
    
    filepath = str(Path(__file__).parent.absolute()) + "\patterns.pdict" # get path to "patterns" subfolder
    with open(filepath, "w") as file:
        file.writelines(fileLines) # write patterns to file
    
    UpdatePatterns() # load contents of patterns.pdict to patternDict for consistency

def SavePattern(_grid, uiGrid):
    folderPath = str(Path(__file__).parent.absolute()) + "\patterns" # get path to "patterns" subfolder
    
    try:
        filepath = app.select_file(save=True, folder=folderPath, filetypes=[ ["2D Patterns (*.pattern)", ".pattern"] ]) + ".pattern" # windows dialogue popup for saving files
    except FileNotFoundError:
        app.error("Invalid filepath", "A valid filepath must be selected to save this file.") # error popup when no file is created
        return

    filename = (Path(filepath).name).replace(".pattern","")
    if filename.rstrip() == "":
        app.error("Invalid filepath", "A valid filename must be entered to save this file.") # error popup when an invalid filename is used
        return
    
    _grid = UItoGrid(_grid, uiGrid) # copy the current UI grid to the mainGrid for continuity
    pattern = CreatePatternAuto(_grid) # automatically generate pattern that contains all alive cells in the smallest dimensions possible
    
    with open(filepath,"x") as file:
        file.write(str(pattern)) # write pattern to file
    
    UpdatePatterns() # load contents of patterns.pdict to patternDict for consistency

def UpdatePatterns():
    global patternDict
    path = str(Path(__file__).parent.absolute()) + "\patterns.pdict"
    patternsCom.clear()
    with open(path, "r") as f:
        patterns = f.readlines()
        print("save patterns :>" + str(patterns))
        for i in range(len(patterns)):
            patterns[i] = patterns[i].split(";")
            print(patterns)

        patternsCom.clear()
        for pattern in patterns:
            patternsCom.append(pattern[0])
            patternDict[pattern[0]] = pattern[1]
    
def PlacePattern(x,y):
    pattern = ""
    try:
        print(str(patternsCom.value))
        print(patternDict[str(patternsCom.value)])
        pattern = patternDict[str(patternsCom.value)]
        print(pattern)
    except KeyError:
        app.error("Invalid Pattern", "No pattern has been selected. Try creating or importing a pattern.")
        return False
        
    if pattern == "":
        app.error("Invalid Pattern", "No pattern has been selected. Try creating or importing a pattern.")
        return False
    _grid = UItoGrid(mainGrid, gameGridWfl)

    pattern = eval(str(pattern))

    if len(pattern[0]) < len(_grid[0])-1 and len(pattern) < len(_grid)-1:
        for _y in range(len(pattern)):
            for _x in range(len(pattern[0])):
                try:
                    print(str(x+_x) + "," + str(y+_y))
                    _grid[y+_y][x+_x] = pattern[_y][_x]
                except IndexError:
                    continue
    
    SetGrid(mainGrid, _grid, gameGridWfl, height=ySld.value, width=xSld.value)


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
    CustomColor() #Update UI grid colours in realtime

def ColorMode2():
    """Set colorMode to 0 (XY Gradient)"""
    global colorMode
    colorMode = 2
    RecolorGrid(gameGridWfl) #Update UI grid colours in realtime

def WaffleClick(x,y):
    """Toggle cells when clicked on the UI grid"""
    if clipboardKey:
        BoundingBox(x,y)
    elif patternKey:
        PlacePattern(x,y)
    else:
        TogglePixel(gameGridWfl, x,y, CellColor(x,y))
        

patternKey = False
def PatternKey():
    global patternKey
    
    if patternKey == False:
        patternKey = True
        clipboardKey = False
        return
    patternKey = False
    
clipboardKey = False
def ClipboardKey():
    global clipboardKey
    
    if clipboardKey == False:
        clipboardKey = True
        patternKey = False
        return
    clipboardKey = False

def Keybind(eventData):
    if eventData.key == "p":
        PatternKey()
    elif eventData.key == "c":
        ClipboardKey()

boundingBoxXY1 = None
boundingBoxXY2 = None
def BoundingBox(x,y):
    global boundingBoxXY1,boundingBoxXY2
    if boundingBoxXY2 == None:
        boundingBoxXY2 = (x,y)
    else:
        boundingBoxXY1 = (x,y)
        boundingBoxXY2 = None

def GenerateGridCall():
    """Call GenerateGrid when generatePB button is pressed"""
    global playSim
    playSim = False
    
    GenerateGrid(mainGrid, gameGridWfl, ySld.value, xSld.value)
       
def UpdateGridCall():
    """Call UpdateGrid when advancePB button is pressed"""
    global playSim
    playSim = False
    
    UpdateGrid(mainGrid, gameGridWfl, gameGridWfl.height, gameGridWfl.width)

playSim = False
def RepeatUpdateGrid():
    """Call UpdateGrid when playSim is enabled"""
    global playSim, playSimDelay
    if playSim:
        UpdateGrid(mainGrid, gameGridWfl, gameGridWfl.height, gameGridWfl.width)
    
def PlaySimCall():
    """Enable playSim when playSimPB button is pressed"""
    global playSim
    playSim = True
    
def StopSimCall():
    """Disable playSim when stopSimPB button is pressed"""
    global playSim
    playSim = False
    
def RandomiseGridCall():
    """Call RandomiseGrid when randomisePB button is pressed"""
    global playSim
    playSim = False
    
    RandomiseGrid(mainGrid, gameGridWfl, gameGridWfl.height, gameGridWfl.width, optionsRandomPageOption1Sld.value)

def SaveSeedCall():
    """Call SaveSeed when "File>Save Seed" is pressed"""
    SaveSeed(mainGrid, gameGridWfl)
    
def LoadSeedCall():
    """Call LoadSeed when "File>Load Seed" is pressed"""
    LoadSeed(mainGrid, gameGridWfl)

def SavePatternCall():
    """Call SavePattern when "Pattern>Export Pattern" is pressed"""
    SavePattern(mainGrid, gameGridWfl)
      
def LoadPatternCall():
    """Call LoadPattern when "Pattern>Import Pattern" is pressed"""
    LoadPattern(mainGrid, gameGridWfl)
    
def PatternToolCall():
    """Enable/Disable patternKey when patternsCB checkbox is pressed"""
    global patternKey
    PatternKey()
    patternsCB.value = False
    if patternKey:
        patternsCB.value = True
        

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
    """Highlight a widget on any event
    
    eventData - data from the widget"""
    eventData.widget.bg = (220,220,220)

def Lowlight(eventData):
    """De-highlight a widget on any event
    
    eventData - data from the widget"""
    eventData.widget.bg = (255,255,255)

### MAIN WINDOW ###
genCount = 0
app = App(title="Conway's Game of Life - Generation 0")
app.bg = "light gray"
app.font = "helvetica"
app.repeat(150, RepeatUpdateGrid)

app.when_key_pressed = Keybind

menuBar = MenuBar(app,
                toplevel=["File", "Pattern", "Colour"], 
                options=[
                    [ ["Options", OptionsPopup], ["Load Seed", LoadSeedCall], ["Save Seed", SaveSeedCall] ], 
                    [ ["Import Pattern", LoadPatternCall], ["Export Pattern", SavePatternCall] ],
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
                        width=20,
                        height=2, 
                        text="Generate Grid", 
                        command=GenerateGridCall)
randomisePB = PushButton(PButtonBox, 
                        grid=[1,0], 
                        width=20,
                        height=2, 
                        text="Randomise Grid", 
                        command=RandomiseGridCall)

advancePB = PushButton(parameterBox,
                       width=44,
                       height=2,
                       text="Advance Generation", 
                       command=UpdateGridCall)

playSimPB = PushButton(parameterBox, 
                       align="left", 
                       width=5,
                       text="⏵", 
                       command=PlaySimCall)

stopSimPB = PushButton(parameterBox,
                       align="left",
                       width=5, 
                       text="⏸", 
                       command=StopSimCall)

generatePB.bg = "white"
generatePB.when_mouse_enters = Highlight
generatePB.when_mouse_leaves = Lowlight

advancePB.bg = "white"
advancePB.when_mouse_enters = Highlight
advancePB.when_mouse_leaves = Lowlight

randomisePB.bg = "white"
randomisePB.when_mouse_enters = Highlight
randomisePB.when_mouse_leaves = Lowlight

playSimPB.bg = "white"
playSimPB.when_mouse_enters = Highlight
playSimPB.when_mouse_leaves = Lowlight

stopSimPB.bg = "white"
stopSimPB.when_mouse_enters = Highlight
stopSimPB.when_mouse_leaves = Lowlight

        # Pattern Tool #
patternsBox = Box(parameterBox, 
                  layout="grid", 
                  border=2, 
                  width="fill",
                  height=44)

patternsBox.bg = "white"
patternsBox.set_border(2,"light gray")
patternsCBT = Text(patternsBox, 
                   grid=[2,0], 
                   text="Pattern Tool")

patternsCB = CheckBox(patternsBox, 
                      grid=[1,0], 
                      command=PatternToolCall)

patternsCom = Combo(patternsBox, 
                    grid=[0,0], 
                    options=[], 
                    selected=0)

patternsCB.bg = "white"
patternsCB.when_mouse_enters = Highlight
patternsCB.when_mouse_leaves = Lowlight

patternsCom.bg = "white"
patternsCom.when_mouse_enters = Highlight
patternsCom.when_mouse_leaves = Lowlight
UpdatePatterns()

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





    
