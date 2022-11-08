from numbers.factors import getFactors 
from argparse import ArgumentParser 

parser = ArgumentParser()

parser.add_argument('--number', '-n', required=True, help='Enter the number to display factor')
args = parser.parse_args()

print(getFactors(int(args.number)))