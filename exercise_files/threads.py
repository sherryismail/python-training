import time
import threading
from multiprocess import Process

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
