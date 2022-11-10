from canvases.canvas import Canvas
from termcolor import colored

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