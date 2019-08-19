"""
Written by Shuyu Tang

main function of CorneringGame
"""
from CorneringGameLib import *

"""Play cornering game."""

# Initialize local variables
size = 5
side1 = "white"
side2 = "black"

ui = CorneringGameUI(CorneringGame(size), side1, side2)
ui.run()        
print "Finished"

