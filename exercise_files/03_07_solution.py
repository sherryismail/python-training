import os
import time
from termcolor import colored
import math #round function


class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]
    
    # convert the float to integer positions for discrete steps
    def hitsWall(self, point):
        return round(point[0])<0 or round(point[0])>=self._x or round(point[1])<0 or round(point[1])>=self._y
    
    # convert the float to integer positions for discrete steps
    def setPos(self, pos, mark):
        self._canvas[round(pos[0])] [round(pos[1])] = mark

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

        self.direction = [0, 0]#new var instead of pos[]

    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]

    def forward(self):
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def up(self):
        self.direction = [0, -1]#remove pos[]
        self.forward()

    def down(self):
        self.direction = [0, 1]#replace pos[]
        self.forward()

    def right(self):
        self.direction = [1, 0]
        self.forward()

    def left(self):
        self.direction = [-1, 0]
        self.forward()
    
    def diagonal(self):
       self.direction = [1,1]
       self.forward()

    def drawSquare(self, size):
        for i in range(size):
            self.right()
        for i in range(size):
            self.down()
        for i in range(size):
            self.left()
        for i in range(size):
            self.up()
        for i in range(size):
            self.diagonal()
        

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)

canvas = Canvas(10, 10)
scribe = TerminalScribe(canvas)
scribe.setDegrees(135)
scribe.drawSquare(5)
# . . . . . .        
# . .       .        
# .   .     .        
# .     .   .        
# .       . .        
# . . . . . *
