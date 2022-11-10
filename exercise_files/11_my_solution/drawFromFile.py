# this is entry point for user to run and pass args
import argparse

# Import these so that we can pass them to "fromFile" as globals
import canvases
from canvases.canvas import Canvas
from canvases.canvasAxis import CanvasAxis 
import scribes
from scribes.terminalScribe import TerminalScribe
from scribes.plotScribe import PlotScribe 
from scribes.randomScribe import RandomWalkScribe
from scribes.robotScribe import RobotScribe, RegularShapes

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', required=False, help='Enter the file name for scribes')
args = parser.parse_args()

print(f'Reading from the file "{args.file}.json" to draw scribes')

canvas = CanvasAxis.fromFile(args.file, globals())
canvas.print()
canvas.go()
