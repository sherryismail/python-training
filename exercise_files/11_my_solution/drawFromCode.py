import scribes
from scribes.terminalScribe import TerminalScribe
from scribes.robotScribe import RobotScribe, RegularShapes
from scribes.randomScribe import RandomWalkScribe
from scribes.plotScribe import PlotScribe
import canvases
from canvases.canvasAxis import CanvasAxis
from canvases.canvas import Canvas 

from utils import sine

scribe1 = TerminalScribe(color='green')
scribe1.forward(10)
regScribe = RegularShapes(color='yellow', pos=[10,10], trailColor='yellow')
regScribe.drawDiamond(10)
scribe3 = PlotScribe(domain=[0, 80], color='cyan', trailColor='green')
scribe3.plotX(sine)
scribe4 = RandomWalkScribe(trail='=', trailColor='magenta')
scribe4.forward(100)
canvas = Canvas(30, 30, scribes=[scribe1, regScribe, scribe3, scribe4])
canvas.toFile('programmed_scribes')

newCanvas = CanvasAxis.fromFile('programmed_scribes', globals())
newCanvas.print()
newCanvas.go()
