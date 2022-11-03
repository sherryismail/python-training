import math
# static methods vs instance methods
# Part of class definition versus a method belongs to object and mutable

class Orientation:
    pi = 3.14
    def __init__(self, x_pos, y_pos, degrees):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dir, self.y_dir = self.getUnitVectorFromDegrees(degrees)
        
    @staticmethod # this is a decorator
    def getUnitVectorFromDegrees(degrees):
        radians = (degrees/180) * Orientation.pi
        return math.sin(radians), -math.cos(radians)
    
    def getNextPos(self):
        return self.x_pos + self.x_dir, self.y_pos + self.y_dir
    
myOrientation = Orientation(5, 5, 75)
myOrientation.getNextPos()

class UniqueList(list):
    # constructor
    def __init__(self):
        super().__init__() #if super.init is not here, all initiationlaisation of parent constructor is overridden
        self.someProperty = 'Unique List!'   

    def append(self, item):
        if item in self:
            return
        super().append(item)
        
uniqueList = UniqueList()
uniqueList.append(1)
uniqueList.append(1)
uniqueList.append(2)

print(uniqueList.someProperty)