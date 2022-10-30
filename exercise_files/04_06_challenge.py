import os
import time
from termcolor import colored
import math 
import time

class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x or round(point[1]) < 0 or round(point[1]) >= self._y

    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.05
        self.pos = [0, 0]

        self.direction = [0, 0]

    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]
    
    def setPosition(self, pos):
        self.pos = pos

    def up(self):
        self.direction = [0, -1]
        self.forward()

    def down(self):
        self.direction = [0, 1]
        self.forward()

    def right(self):
        self.direction = [1, 0]
        self.forward()

    def left(self):
        self.direction = [-1, 0]
        self.forward()
    
    def diagonal_down_right(self):
       self.direction = [1,1]
       self.forward()
    
    def diagonal_up_right(self):
       self.direction = [1,-1]
       #x=1 so cursor moves right
       #y=-1 so it moves up
       self.forward()

    def diagonal_up_left(self):
       self.direction = [-1,-1]
       self.forward()

    def diagonal_down_left(self):
       self.direction = [-1,1]
       self.forward()

    def forward(self):
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)
    
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
            self.down()
        for i in range(size):
            self.diagonal_up_right()
        for i in range(size):
            self.diagonal_down_right()
        for i in range(size):
            self.diagonal_down_left()
        for i in range(size):
            self.diagonal_up_left()

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)

canvas = Canvas(30,20)

# scribes is a list of shapes. Each shape is a dictionary entry.
# type(scibes[0]) is a dictionary of features. scribes[0]['position'] is a list
scribes = [
    {'name': 'square',
    'degrees':0,
    'position': [0,0],
    'instructions': [
        {'direction':'right', 'duration':5},
        {'direction':'down', 'duration':5},
        {'direction':'left', 'duration':5},
        {'direction':'up', 'duration':5}
        ],
      },
    {'name': 'diamond',
    'degrees':30,
    'position': [5,5],
    'instructions': [
        {'direction':'diagonal_up_right', 'duration':5},
        {'direction':'diagonal_down_right', 'duration':5},
        {'direction':'diagonal_down_left', 'duration':5},
        {'direction':'diagonal_up_left', 'duration':5}
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

for scribeData in scribes:
    print(scribeData['name'])
    time.sleep(0.5) #instantiate a new scribe object
    scribeData['name'] = TerminalScribe(canvas)
    scribeData['name'].setDegrees(scribeData['degrees'])
    scribeData['name'].setPosition(scribeData['position'])
    # Flatten instructions: so cursors of all scribes move at the same time
    # Convert "{'left': 10}" to ['left', 'left', 'left'...]
    scribeData['instructions_flat'] = []
    for instruction in scribeData['instructions']:
        scribeData['instructions_flat'] = scribeData['instructions_flat'] + [instruction['direction']]*instruction['duration']
        # append to the instrcutions_flat list, each direction as a string, multiplied by duration times

maxInstructionLength = max([len(scribeData['instructions_flat']) for scribeData in scribes])

for i in range(maxInstructionLength):
    for scribeData in scribes:
        if i < len(scribeData['instructions_flat']):
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

