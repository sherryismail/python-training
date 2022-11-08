from numbers.factors import getFactors
# this is a module
# def isPrime(n, foundPrimes=None):
#     foundPrimes = range(2, int(n**0.5)) if foundPrimes is None else foundPrimes
#     for factor in foundPrimes:
#         if n % factor == 0:
#             return False
#     return True

def isPrime(n, foundPrimes=None):
    return len(getFactors(n)) == 2

def listPrimes(max):
    foundPrimes = []
    for n in range(2, max):
        if isPrime(n, foundPrimes):
            foundPrimes.append(n)
    return foundPrimes
    
print(f'primes.py module name is {__name__}')

if __name__ == '__main__':
    print('This is a module. Please import using\n import primes')
    #  >>python exercise_files/11_02_e/primes.py