import os
import time
from termcolor import colored, COLORS
import math 
import random
from threading import Thread
from inspect import getmembers, ismethod
import json

class TerminalScribeException(Exception):
    def __init__(self, message=''):
        super().__init__(colored(message, 'red'))

class InvalidParameter(TerminalScribeException):
    pass

def is_number(val):
    try:
        float(val)
        return True
    except ValueError:
        return False

class Canvas:
    def __init__(self, width, height, scribes=[], framerate=.05):
        if not is_number(width):
            raise InvalidParameter('Width must be a number')
        self._x = width
        if not is_number(height):
            raise InvalidParameter('Height must be a number')
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]
        self.scribes = scribes

        if not is_number(framerate):
            raise InvalidParameter('Framerate must be a number')
        self.framerate = framerate

    def toDict(self):
        return {
            'classname': type(self).__name__,
            'x': self._x,
            'y': self._y,
            'canvas': self._canvas,
            'scribes': [scribe.toDict() for scribe in self.scribes]
        }

    def fromDict(data):
        # print('canvas name='+globals()[data.get('classname')].__name__)
        # for scribe in data.get('scribes'): #debug prints
        #     print('scribe name='+scribe.get('classname'))
        canvas = globals()[data.get('classname')](data.get('x'), data.get('y'), scribes=[globals()[scribe.get('classname')].fromDict(scribe) for scribe in data.get('scribes')])
        canvas._canvas = data.get('canvas')
        return canvas

    def toFile(self, name):
        with open(name+'.json', 'w') as f:
            f.write(json.dumps(self.toDict()))

    def fromFile(name): # static method so no 'self' arg
        with open(name+'.json', 'r') as f:
            try:
                return Canvas.fromDict(json.loads(f.readline()))
            except:
                raise TerminalScribeException('File {}.json is not a valid Scribe file'.format(name))

    def hitsVerticalWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x

    def hitsHorizontalWall(self, point):
        return round(point[1]) < 0 or round(point[1]) >= self._y

    def hitsWall(self, point):
        return self.hitsVerticalWall(point) or self.hitsHorizontalWall(point)

    def getReflection(self, point):
        return [-1 if self.hitsVerticalWall(point) else 1, -1 if self.hitsHorizontalWall(point) else 1]

    def setPos(self, pos, mark):
        try:
            self._canvas[round(pos[0])][round(pos[1])] = mark
        except Exception as e:
            raise TerminalScribeException(e)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def go(self):
        max_moves = max([len(scribe.moves) for scribe in self.scribes])
        for i in range(max_moves):
            for scribe in self.scribes:
                threads = []
                if len(scribe.moves) > i: # assemble the args needed for each move and args 'self'
                    args = scribe.moves[i][1]+[self]
                    # print(f'{scribe.moves[i][0].__name__} and {scribe.moves[i][1]}') #print the classname of scribe
                    # print(f'Total scibes= {len(self.scribes)}')
                    # scribe.moves[i][0](*args)# call the func pointer 'moves[i][0]()' and pass args
                    threads.append(Thread(target=scribe.moves[i][0], args=args))
                [thread.start() for thread in threads]
                [thread.join() for thread in threads]
            self.print()
            time.sleep(self.framerate)

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))
    
class CanvasAxis(Canvas):
    # Pads 1-digit numbers with an extra space
    def formatAxisNumber(self, num):
        if num % 5 != 0:
            return '  '
        if num < 10:
            return ' '+str(num)
        return str(num)

    def print(self):
        self.clear()
        for y in range(self._y):
            print(colored(self.formatAxisNumber(y) + ' '.join([col[y] for col in self._canvas]), 'blue'))
         # reached bottom of canvas, print x-axis

        print(colored(' '.join([self.formatAxisNumber(x) for x in range(self._x)]),'blue'))

class TerminalScribe:
    def __init__(self, color='red', mark='*', trail='.', pos=(0, 0), degrees=135, trailColor='red'):
        self.moves = []

        if color not in COLORS:
            raise InvalidParameter(f'color {self.color} not a valid color ({", ".join(list(COLORS.keys()))})')
        self.color=color

        if len(str(mark)) != 1:
            raise InvalidParameter('Mark must be a single character')
        self.mark = str(mark)

        if len(str(trail)) != 1:
            raise InvalidParameter('Trail must be a single character')
        self.trail = str(trail)

        if trailColor not in COLORS:
            raise InvalidParameter(f'Color {trailColor} is not from the list ({",".join(list(COLORS.keys()))})')   
        self.trailColor = trailColor
        
        if len(pos) != 2 or not is_number(pos[0])or not is_number(pos[1]):
            raise InvalidParameter('Position must be two numeric values (x, y)')
        self.pos = pos
        
        if not is_number(degrees):
            raise InvalidParameter('Degrees must be a valid number')
        self.setDegrees(degrees)

    def toDict(self):
        return {
            'classname': type(self).__name__,
            'color': self.color,
            'mark': self.mark,
            'trail': self.trail,
            'trailColor': self.trailColor,
            'pos': self.pos,
            'moves': [[move[0].__name__, move[1]] for move in self.moves]#move[0]= func, move[1] = args
        }

    def fromDict(data):
        scribe = globals()[data.get('classname')](
            color=data.get('color'),
            mark=data.get('mark'),
            trail=data.get('trail'),
            trailColor=data.get('trailColor'),
            pos=data.get('pos'),
            )
        scribe.moves = scribe._movesFromDict(data.get('moves'))
        return scribe

    def _movesFromDict(self, movesData): # bind the moves to the scribes as func, not just the string
        # for key, val in getmembers(self, predicate=ismethod):
        #     print(key+' <-key:val->'+str(type(val)))
        bound_methods = {key: val for key, val in getmembers(self, predicate=ismethod)}
        return [[bound_methods[name], args] for name, args in movesData] # advanced

    def _setPosition(self, pos, _):
        self.pos = pos

    def setPosition(self, pos):
        self.moves.append((self._setPosition, [pos]))

    def _setDirection(self, direction, _):
        self.direction = direction

    def setDirection(self, direction):
        self.moves.append((self._setDirection, [direction]))

    def degreesToUnitDirection(self, degrees):
        radians = (degrees/180) * math.pi 
        return [math.sin(radians), -math.cos(radians)]

    def _setDegrees(self, degrees, _):
        self.direction = self.degreesToUnitDirection(degrees)
    
    def setDegrees(self, degrees):
        self.moves.append((self._setDegrees, [degrees]))

    def bounce(self, pos, canvas):
        reflection = canvas.getReflection(pos)
        self.direction = [self.direction[0] * reflection[0], self.direction[1] * reflection[1]]

    def _forward(self, canvas):
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        if canvas.hitsWall(pos):
            self.bounce(pos, canvas)
            pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        self.draw(pos, canvas)

    def forward(self, distance=1):
        for i in range(distance):
            self.moves.append((self._forward, []))

    def draw(self, pos, canvas):
        canvas.setPos(self.pos, colored(self.trail, self.trailColor))
        self.pos = pos
        canvas.setPos(self.pos, colored(self.mark, self.color))

class PlotScribe(TerminalScribe):

    def __init__(self, domain, **kwargs):
        self.x = domain[0]
        self.domain = domain
        super().__init__(**kwargs)

    def toDict(self):
        data = super().toDict()
        data['x'] = self.x 
        data['domain'] = self.domain
        return data

    def fromDict(data):
        scribe = globals()[data.get('classname')](
            color=data.get('color'),
            mark=data.get('mark'),
            trail=data.get('trail'),
            trailColor=data.get('trailColor'),
            pos=data.get('pos'),
            domain=data.get('domain'),
        )
        scribe.moves = scribe._movesFromDict(data.get('moves'))#important, missing before
        scribe.x = data.get('x')
        return scribe

    def _plotX(self, pos, canvas):
        if canvas.hitsWall(pos): 
            try:
                super().bounce(pos, canvas)
                if int(pos[0]/canvas._x) % 2 == 0: #if y=0, bounce forwards
                    horizontal = pos[0] % canvas._x
                    self.x = horizontal # back to normal
                else: #or if y=MAX wall, bounce backwards
                    horizontal = int(canvas._x - (pos[0] %canvas._x) -1)
                new_pos = [horizontal, pos[1]]
                self.draw(new_pos, canvas)
            except Exception as e:
                print(e)
        else:
            self.draw(pos, canvas)
        # self.x = self.x + 1 #remove this because x is incremented from plotX()

    def plotX(self, function):
        self.x = self.domain[0]
        for x in range(self.domain[0], self.domain[1]):
            pos = [x, function(x)]
            self.moves.append((self._plotX, [pos]))# not (self._plotX, [function(x)]))
        #TypeError: Object of type function is not JSON serializable if [function] or function[(x)]
class RobotScribe(TerminalScribe):    
    def up(self, distance=1):
        self.setDirection([0, -1])
        self.forward(distance)

    def down(self, distance=1):
        self.setDirection([0, 1])
        self.forward(distance)

    def right(self, distance=1):
        self.setDirection([1, 0])
        self.forward(distance)

    def left(self, distance=1):
        self.setDirection([-1, 0])
        self.forward(distance)
    
    def diagonal_down_right(self, distance=1):
        self.setDirection([1,1])
        self.forward(distance)
    
    def diagonal_up_right(self, distance=1):
        self.setDirection([1,-1]) #x=1 so cursor moves right
        self.forward(distance)#y=-1 so it moves up
    
    def diagonal_up_left(self, distance=1):
        self.setDirection([-1,-1])
        self.forward(distance)

    def diagonal_down_left(self, distance=1):
        self.setDirection([-1,1])
        self.forward(distance)

class RegularShapes(RobotScribe):
    def __init__(self,*args, **kwargs):#kwargs for trail=, color=:
        super().__init__(*args, **kwargs)
    def drawSquare(self, size):
        self.right(size)
        self.down(size)
        self.left(size)
        self.up(size)

    def drawDiamond(self, size):
        self.diagonal_up_right(size)
        self.diagonal_down_right(size)
        self.diagonal_down_left(size)
        self.diagonal_up_left(size)

class RandomShapes(RobotScribe, TerminalScribe):
    def __init__(self,scribes,*args, **kwargs):#kwargs for trail=, color=:
        super().__init__(*args, **kwargs)
        self.scribes = scribes
    
    def unpackDictionary(self):
        for info in self.scribes:
            print(info['name'])
            self.flattenInstructions(scribeData=info)

    def flattenInstructions(self, scribeData):
        scribeData['instructions_flat'] = []
        for instruction in scribeData['instructions']:
            scribeData['instructions_flat'] = scribeData['instructions_flat'] + [instruction['direction']]*instruction['duration']
            # append to the instrcutions_flat list, each direction as a string, multiplied by duration times

        for i in range(len(scribeData['instructions_flat'])):
            if scribeData['instructions_flat'][i] == 'forward':
                self.forward() # instead of scribeData['name'].forward(1)
            if scribeData['instructions_flat'][i] == 'up':
                self.up()
            elif scribeData['instructions_flat'][i] == 'down':
                self.down()
            elif scribeData['instructions_flat'][i] == 'left':
                self.left()
            elif scribeData['instructions_flat'][i] == 'right':
                self.right()
            if scribeData['instructions_flat'][i] == 'diagonal_up_right':
                self.diagonal_up_right()
            elif scribeData['instructions_flat'][i] == 'diagonal_down_right':
                self.diagonal_down_right()
            elif scribeData['instructions_flat'][i] == 'diagonal_up_left':
                self.diagonal_up_left()
            elif scribeData['instructions_flat'][i] == 'diagonal_down_left':
                self.diagonal_down_left()
            
        print(len(scribeData['instructions_flat']))
        time.sleep(2)

class RandomWalkScribe(TerminalScribe):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.degrees = kwargs.get('degrees', 135)
    
    def _randomizeDegrees(self, _):
        self.degrees = random.randint(self.degrees-10, self.degrees+10)
        self.direction = self.degreesToUnitDirection(self.degrees)
        print(f'Degrees is {self.degrees}')

    def randomizeDegrees(self):
        self.moves.append((self._randomizeDegrees, []))
    
    def bounce(self, pos, canvas):
        reflection = canvas.getReflection(pos)
        if reflection[0] == -1:
            self.degrees = 360 - self.degrees
        if reflection[1] == -1:
            self.degrees = 180 - self.degrees
        self.direction = [self.direction[0] * reflection[0], self.direction[1] * reflection[1]]

    def forward(self, distance=1):
        for i in range(distance):
            self.randomizeDegrees()
            super().forward()

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
    'degrees':45,
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

scribe1 = TerminalScribe(color='green')
scribe1.forward(100)
scribe2 = RegularShapes(color='yellow', pos=[10,10], trailColor='yellow')
scribe2.drawDiamond(10)
scribe3 = PlotScribe(domain=[0, 80], color='cyan', trailColor='green')
scribe3.plotX(sine)
scribe4 = RandomWalkScribe(trail='-', trailColor='magenta')
scribe4.forward(100)
scribe5 = RandomWalkScribe(trail='=',color='blue')
scribe5.forward(100)
# scribe6 = RandomShapes(trailColor='red',trail='+', scribes=randomScribes)
# scribe6.unpackDictionary() #TODO

canvas1 = CanvasAxis(30, 30, scribes=[scribe1, scribe2, scribe3, scribe4, scribe5])
canvas1.toFile('solution_my_10')

canvas2 = Canvas.fromFile('solution_my_10')
canvas2.go()