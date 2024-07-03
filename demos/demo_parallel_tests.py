"""Demo uses multiprocessing."""

import time
import multiprocessing

def useless_function(sec = 1):
    """Useless function"""
    print(f'Sleeping for {sec} second(s)')
    time.sleep(sec)
    print(f'Done sleeping for {sec} second(s)')

start = time.perf_counter()

process1 = multiprocessing.Process(target=useless_function, args=(1,))
process2 = multiprocessing.Process(target=useless_function, args=(5,))

process1.start()
process2.start()

end = time.perf_counter()

print(f'Finished in {round(end-start, 2)} second(s)')

# OUTPUT:
# Finished in 0.1 second(s)
# Sleeping for 1 second(s)
# Sleeping for 5 second(s)
# Done sleeping for 1 second(s)
# Done sleeping for 5 second(s)
