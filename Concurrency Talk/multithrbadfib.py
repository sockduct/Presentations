# Broken Multi-threaded fibonacci server
#
# Illustrates common mistake for concurrent code with threads/
# processes - see multithrfib.py for correct implementation
#
# Created for Concurrent Python presentation
#
# Based on examples/code from David Beazley including following:
# * Fear and Awaiting in Async (Screencast)
#   (https://www.youtube.com/watch?v=Bm96RqNGbGo)
# * Keynote David Beazley - Topics of Interest (Python Asyncio)
#   (https://www.youtube.com/watch?v=ZzfHjytDceU)
# * David Beazley - Python Concurrency From the Ground Up: LIVE!
#  - PyCon 2015 (https://www.youtube.com/watch?v=MCs5OvhV9S4)
#
from fib import fib
import time
from threading import Thread

def dispatcher(flist):
    dthreads = []
    for fnum in flist:
        t = Thread(target=fib, args=(fnum,))
        dthreads.append(t)
        t.start()

myfibs = [36, 36, 36, 36]
start = time.time()
dispatcher(myfibs)
end = time.time()
print('Ellapsed time:  {}'.format(end - start))

