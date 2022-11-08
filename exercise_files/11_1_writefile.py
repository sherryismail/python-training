from argparse import ArgumentParser 

parser = ArgumentParser()

parser.add_argument('--output', '-o', required=True, help='The destination file for the output of this program')
parser.add_argument('--content', '-c', required=True, help='The text to write to the file')


args = parser.parse_args()

with open(args.output , 'w') as f:
    f.write(args.content+'\n')

print(f'Wrote "{args.content}" to file "{args.output}"')