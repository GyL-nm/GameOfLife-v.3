import math
from pathlib import Path
from guizero import App, Window, Box, Text, PushButton, TextBox, Slider, Waffle, MenuBar, Combo, CheckBox

import grid
import ui

test = False

def UpdateGrid(_grid):
    grid.UpdateGrid(_grid)
    ui.UpdateGrid(_grid, ui.ySld.value, ui.xSld.value)
    
mainGrid = grid.GenerateGrid(25,25)
ui.Display()

if test:
    testGrid = grid.GenerateGrid(10,10)
    grid.Print2dArray(testGrid)