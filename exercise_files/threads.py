import time
import threading
from multiprocess import Process
import csv

def longSquare(num, results):
    results[num] = num**2 # if it was return n**2, thread won't hold result

results = {} # common external memory needed between two threads
[longSquare(n,results) for n in range(0, 3)] # takes a long time
print(f'When just two functions: {results}')

# args is a Tuple so avoid confusion by not using args=(1)
t1 = threading.Thread(target=longSquare, args=(1,results))
t2 = threading.Thread(target=longSquare, args=(2,results))

t1.start()
t2.start()
t1.join()
t2.join()
print(f'When two threads run parallel: {results}')

##############################
# same processor will execute a statement from t1, t2, t3 and t1 again and picks them up in round-robin. If t1 were time.sleep
# emulates parallel computing
threads = [threading.Thread(target=longSquare, args=(n, results)) for n in range(0, 10)]
[t.start() for t in threads]
[t.join() for t in threads]
print(f'When ten threads run parallel: {results}')

##############################
# tasks in parallel. processes dont share memory so results will be empty.
# but if there were a file system to share information
results = {}
processes = [Process(target=longSquare, args=(n,results)) for n in range(0, 10)]
[p.start() for p in processes]
[p.join() for p in processes]
print(f'When 10 Processes run parallel: {results}')

##################### CSV Reading
import csv
from itertools import islice
with open('exercise_files/10_02_us.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)
    next(reader)
    for count,row in islice(enumerate(reader),1,10):#but how to limit 1,100
        print(f'{count} ==> {row}')

    ################# Open CSV and store dict
with open('exercise_files/10_02_us.csv', 'r') as f:
    data = list(csv.DictReader(f, delimiter='\t'))
    #next(reader)##TypeError: '_csv.reader' object is not subscriptable
    for row in islice(data,1,10):
        print(row)

primes = []

for number in range(2, 99999):
    for factor in range(2, int(number**0.5) + 1):
        if number % factor == 0:
            break
    else:
        primes.append(number)

data = [row for row in data if int(row['postal code']) in primes and row['state code'] == 'MA']

# Writing CSV
with open('exercise_files/10_02_ma_prime_new.csv', 'w') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow([row['place name'], row['county']])#default delimiter is comma
        print(row)