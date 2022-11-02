import os
import time
from termcolor import colored
import math 


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
            print(' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.05
        self.pos = [0, 0]

        self.direction = [0, 1]

    def setPosition(self, pos):
        self.pos = pos

    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]

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

    def drawSquare(self, size):
        for i in range(size):
            self.right()
        for i in range(size):
            self.down()
        for i in range(size):
            self.left()
        for i in range(size):
            self.up()

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)

    def plotX(self, function):
        for x in range(1, 2* self.canvas._x):#exceed limit to check bounce
            pos = [x, function(x)]
            if not self.canvas.hitsWall(pos):
                self.draw(pos)
            else:#TODO: bounce back from wall
                pos = [x, function(x)]
    
    def drawAxis(self):
        for n in range(1,self.canvas._x):
            pos=[n, 0]
            if n % 10 == 0:
                self.canvas.setPos(pos, colored(n, 'blue'))
            else:
                self.canvas.setPos(pos, colored(self.trail, 'blue'))
            self.canvas.print()
            time.sleep(self.framerate)
        for n in range(1,self.canvas._y):
            pos=[0, n]
            if n % 10 == 0:
                self.canvas.setPos(pos, colored(n, 'blue'))
            else:
                self.canvas.setPos(pos, colored(self.trail, 'blue'))
            self.canvas.print()
            time.sleep(self.framerate)

def sine(x):
    return math.sin(x/3) * 4 + 10
def cosine(x):
    return math.cos(x/3) * 4 + 10

canvas = Canvas(30, 15)
scribe = TerminalScribe(canvas)
scribe.drawAxis()
scribe.plotX(sine)
scribe.plotX(cosine)


