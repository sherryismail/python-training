from datetime import datetime
from math import prod
# ternary (having three inputs) operator
n=4
fizzBuzz = 'Fizz' if n%3 ==0 else n
wait_until = datetime.now().second + 2

while True:
    if datetime.now().second < wait_until:
        continue
    break

print(f'We are at {wait_until} seconds!')

animalLookup = {
    'a': ['aardvark', 'antelope'],
    'b': ['bear'],
    'c': ['cat'],
    'd': ['dog'],
}

for letter, animals in animalLookup.items():
    if len(animals) > 1:
        continue # skip execute loop for 'a'. but if it is 'pass'
    print(f'Only one animal: {animals[0]}')

for letter, animals in animalLookup.items():
    if len(animals) > 1:
        print(f'Found {len(animals)}: {animals}')
        break
# Find out Prime numbers in the range 
for number in range(2, 100):
    found_factors = False
    for factor in range(2, int(number**0.5) + 1): # power **
        if number % factor == 0:
            found_factors= True
            break
    if not found_factors:
        print(f'{number} is prime!')

# anatomy of a function
def performOperation(*args, **kwargs): 
    # args= then error if we call perform(1,2)
    # kwargs= otherwise 'got an unexpected keyword argument'
    print(f'args are: {args}')
    print(f'kwargs are: {kwargs}')
    print(f'locals() are: {locals()}')
    
performOperation(1,2,3,operation='sum')

def performOperation2(*args, operation='sum'):
    if operation == 'sum':
        return sum(args)
    if operation == 'multiply':
        return prod(args)
    
print(performOperation2(2,3,3, operation='sum'))

# function as a variable
def removeShortWords(text):
    return ' '.join([word for word in text.split() if len(word) > 3])

processingFunctions = [performOperation, performOperation2]
text = '''A quick Brown fox
jumps over the lazy dog'''
for func in processingFunctions:
    text = func(1,2,3,operation='sum')
# use of lamba function
(lambda x: x+3) (3)
myList = [{'num': 9}, {'num': 4}, {'num': 7}]
# sort the dictionary in ascending order
print(sorted(myList, key=lambda x: x['num'], reverse=False))