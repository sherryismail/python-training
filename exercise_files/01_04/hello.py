
# Print "Hello, World!" to the terminal
from decimal import Decimal, getcontext
my_dictionary = {
    'apple': 'A red fruit', 
    'bear': 'A scary animal',
    'apple': 'Sometimes a green fruit'
}
my_dictionary.update({'car':'a moving object'})
for x,y in my_dictionary.items():
    print(x,y)

int('1ab', 16)
print(Decimal(3.14))
print(Decimal('3.14'))
