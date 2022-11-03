import os
import time
from termcolor import colored
import math 

# graphing scribe, robot scribe
# create interface with termcolor
# allow users to set framerate, pos, and direction
class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsVerticalWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x

    def hitsHorizontalWall(self, point):
        return round(point[1]) < 0 or round(point[1]) >= self._y

    def hitsWall(self, point):
        return self.hitsVerticalWall(point) or self.hitsHorizontalWall(point)

    def getReflection(self, point):
        return [-1 if self.hitsVerticalWall(point) else 1, -1 if self.hitsHorizontalWall(point) else 1]

    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(','.join([col[y] for col in self._canvas]))

class CanvasAxis(Canvas):
    # better to remove framerate so axis appear instantly
    def formatAxisNumber(self, num):
        if num % 5 == 0:
            return str(num)
        return '  '
    def print(self):
        self.clear()
        for y in range(self._y):
            print(colored(self.formatAxisNumber(y) + ' '.join([col[y] for col in self._canvas]), 'blue'))
        # reached bottom of canvas, print x-axis
        print(colored(' '.join([self.formatAxisNumber(x) for x in range(self._x)]),'blue'))

class TerminalScribe:
    def __init__(self, canvas, trail='.',mark='*',framerate=0.05, color='red', trailColor='white',user_pos=[0,0],user_direction=[0,1]):
        self.canvas = canvas
        self.trail = trail
        self.trailColor = trailColor
        self.mark = mark
        self.framerate = framerate
        self.pos = user_pos
        self.color = color
        self.direction = user_direction

    def setPosition(self, pos):
        self.pos = pos
    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]
    def bounce(self, pos):
        reflection = self.canvas.getReflection(pos)
        self.direction = [self.direction[0] * reflection[0], self.direction[1] * reflection[1]]
    def forward(self, distance):
        for i in range(distance):
            pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            if self.canvas.hitsWall(pos):
                self.bounce(pos)
                pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            self.draw(pos)

    def draw(self, pos):
        self.canvas.setPos(self.pos, colored(self.trail, self.trailColor))
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)

class RobotScribe(TerminalScribe):
    def __init__(self,canvas,*args, **kwargs):#kwargs for trail=, color=:
        super().__init__(canvas, *args, **kwargs)
    
    def up(self):
        self.direction = [0, -1]
        self.forward(1)

    def down(self):
        self.direction = [0, 1]
        self.forward(1)

    def right(self):
        self.direction = [1, 0]
        self.forward(1)

    def left(self):
        self.direction = [-1, 0]
        self.forward(1)

    def diagonal_down_right(self):
       self.direction = [1,1]
       self.forward(1)
    
    def diagonal_up_right(self):
       self.direction = [1,-1]
       #x=1 so cursor moves right
       #y=-1 so it moves up
       self.forward(1)

    def diagonal_up_left(self):
       self.direction = [-1,-1]
       self.forward(1)

    def diagonal_down_left(self):
       self.direction = [-1,1]
       self.forward(1)

class PlotScribe(TerminalScribe):
    def plotX(self, function):
        for x in range(self.canvas._x):
            pos = [x, function(x)]
            if pos[1] and not self.canvas.hitsWall(pos):
                self.draw(pos)

class RegularShapes(RobotScribe):
    def drawSquare(self, size):
        for i in range(size):
            self.right()
        for i in range(size):
            self.down()
        for i in range(size):
            self.left()
        for i in range(size):
            self.up()

    def drawDiamond(self, size):
        for i in range(size):
            self.diagonal_up_right()
        for i in range(size):
            self.diagonal_down_right()
        for i in range(size):
            self.diagonal_down_left()
        for i in range(size):
            self.diagonal_up_left()

class RandomShapes(RobotScribe):
    def __init__(self,canvas,scribes,*args, **kwargs):#kwargs for trail=, color=:
        super().__init__(canvas, *args, **kwargs)
        self.scribes = scribes

    def flattenInstructions(self, scribeData):
        scribeData['instructions_flat'] = []
        for instruction in scribeData['instructions']:
            scribeData['instructions_flat'] = scribeData['instructions_flat'] + [instruction['direction']]*instruction['duration']
            # append to the instrcutions_flat list, each direction as a string, multiplied by duration times

def sine(x):
    return 5*math.sin(x/4) + 15

def cosine(x):
    return 5*math.cos(x/4) + 15

def circleTop(x):
    radius = 10
    center = 20
    if x > center - radius and x < center + radius:
        return center-math.sqrt(radius**2 - (x-center)**2)

def circleBottom(x):
    radius = 10
    center = 20
    if x > center - radius and x < center + radius:
        return center+math.sqrt(radius**2 - (x-center)**2)

randomScribes = [
    {'name': 'randomwalk',
    'degrees':135,
    'position': [0,0],
    'instructions': [
        {'direction':'forward', 'duration':50},
        ],
      },
    {'name': 'zigzag',
    'degrees':30,
    'position': [20,10],
    'instructions': [
        {'direction':'diagonal_up_left', 'duration':3},
        {'direction':'diagonal_down_left', 'duration':3},
        {'direction':'diagonal_up_left', 'duration':3},
        {'direction':'diagonal_down_left', 'duration':3},
        {'direction':'diagonal_up_left', 'duration':3},
        {'direction':'diagonal_down_left', 'duration':3}
        ],
      }
    ]

# Canvas and TerminalScribe are not instantiated directly
canvas = CanvasAxis(30, 30)
scribe = PlotScribe(canvas, color='green',trail='-', trailColor='magenta')
scribe.plotX(sine)
#scribe.plotX(circleTop)
scribe.plotX(circleBottom)
shape = RegularShapes(canvas, trailColor='red',color='green',user_pos=[10,10])
shape.drawDiamond(8)

for scribeData in randomScribes:
    print(scribeData['name'])
    time.sleep(0.5) #instantiate a new scribe object
    scribeData['name'] = RandomShapes(canvas,scribes=randomScribes, trail='+', trailColor='green')
    scribeData['name'].setDegrees(scribeData['degrees'])
    scribeData['name'].setPosition(scribeData['position'])
    # Flatten instructions: so cursors of all scribes move at the same time
    # Convert "{'left': 10}" to ['left', 'left', 'left'...]
    scribeData['name'].flattenInstructions(scribeData)

maxInstructionLength = max([len(scribeData['instructions_flat']) for scribeData in randomScribes])

for i in range(maxInstructionLength):
    for scribeData in randomScribes:
        if i < len(scribeData['instructions_flat']):
            if scribeData['instructions_flat'][i] == 'forward':
                scribeData['name'].forward(1)
            if scribeData['instructions_flat'][i] == 'up':
                scribeData['name'].up()
            elif scribeData['instructions_flat'][i] == 'down':
                scribeData['name'].down()
            elif scribeData['instructions_flat'][i] == 'left':
                scribeData['name'].left()
            elif scribeData['instructions_flat'][i] == 'right':
                scribeData['name'].right()
            if scribeData['instructions_flat'][i] == 'diagonal_up_right':
                scribeData['name'].diagonal_up_right()
            elif scribeData['instructions_flat'][i] == 'diagonal_down_right':
                scribeData['name'].diagonal_down_right()
            elif scribeData['instructions_flat'][i] == 'diagonal_up_left':
                scribeData['name'].diagonal_up_left()
            elif scribeData['instructions_flat'][i] == 'diagonal_down_left':
                scribeData['name'].diagonal_down_left()



