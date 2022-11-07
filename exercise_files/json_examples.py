import json
from json import JSONDecodeError, JSONEncoder
jsonString = '{"a": "apple", "b": "bear", "c": "cat",}' #<- due to comma
try:
    json.loads(jsonString)
except JSONDecodeError:
    print('Could not parse JSON!') # should be printed
class Animal:
    def __init__(self, name):
        self.name = name

class AnimalEncoder(JSONEncoder):
    def default(self, o):
        if type(o) == Animal:
            return o.name # so that json can carrry on
        return super().default(o)# if its not animal, let parent deal with it
    
pythonDict = {'a': Animal('aardvark'), 'b': Animal('bear'), 'c': Animal('cat'),}
print(json.dumps(pythonDict, cls=AnimalEncoder))#python->json does not need try-exception
print(globals())