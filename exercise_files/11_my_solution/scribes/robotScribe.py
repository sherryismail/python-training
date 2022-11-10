from scribes.terminalScribe import TerminalScribe
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