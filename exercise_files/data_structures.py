
from collections import defaultdict
from sys import set_asyncgen_hooks
mySet = {'a', 'b', 'c'}
mySet = set(('a', 'b', 'c'))
#mySet[0] is not subscriptable
mySet.add('d')
if 'a' in mySet:
    print(True)
myList = ['a', 'b', 'b', 'c', 'c']
myList = list(set(myList))
while len(mySet):
    mySet.pop()

mylist=[1,2,3,4,5,6,7,8,9,10]
#[::2] is like i+=2. 
# Empty colons means start and end of array are implicit bounds
# negative index makes for-loop traverse in reverse index
for i in mylist[::-2]:
    print(i)
mylist.insert(3, 'a new value') # at index = 3
print(mylist)
print(mylist.pop()) # last value

mylist.append(11)
print(mylist.pop()) 
mypointer = mylist
mycopy = mylist.copy()

myTuple = ('a', 'b', 'c')
print(type(myTuple))

def returnsMultipleValues():
    return 1,2,3

type(returnsMultipleValues())
a, b, c = returnsMultipleValues()
print(a)
print(b)
print(c)

animals = {
    'a': 'aardvark',
    'b': 'bear',
    'c': 'cat',
}
print('Dictionary data struct: \'a\' for '+animals['a'])
animals.get('e', 'elephant') # return elephant as default if None found
# convert dictionary to list
# a dictionary of Lists
animals = {
    'a': ['aardvark','antelope'],
    'b': ['bear'],
}
animals['b'].append('bison') #for appending more
animals['c'] = 'cat' #for new items use equal sign

animals = defaultdict(list) # this creates a new list empty


myList = list(range(100))
filteredList = [item for item in myList if item % 10 == 0]
print(filteredList)
myString = 'My name is Ryan Mitchell. I live in Boston'
def cleanWord(word):
    return word.replace('.', '').lower()

# [cleanWord(word) for word in myString.split()]
# ['my', 'name', 'is', 'ryan', 'mitchell', 'i', 'live', 'in', 'boston']
# all of it in one line
# [cleanWord(word) for word in myString.split() if len(cleanWord(word)<3)]
# ['my', 'is', 'i', 'in']

# Nested list comprehension
# list of lists
[[cleanWord(word) for word in sentence.split()] for sentence in myString.split('.')]

# Convert list to dictionary
animalList = [('a', 'aardvark'), ('b', 'bear'), ('c', 'cat'), ('d', 'dog')]
animalList.append({'e','elephant'})
# animalDict = {item[0]: item[1] for item in animalList}
# whatever is between 'for' and 'in', is what each tuple of animalList is assigned as an identifier
animalDict = {key: value for key,value in animalList}
list(animalDict.items())
print(animalDict.get('a'))

#convert list to dict
values = [[1, 'i', 'a'], ['2', 'we', 'be', 'it'], [3, 'are', 'few', 'too']]
# {
#         1: ['i', 'a'],
#         2: ['we', 'be', 'it'],
#         3: ['are', 'few', 'too']
# }
valuesDict = {item[0]: item[1:] for item in values}
print(type(valuesDict))