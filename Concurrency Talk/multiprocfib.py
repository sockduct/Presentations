# Multi-processing fibonacci server
#
# Created for Concurrent Python presentation
#
# Based on examples/code from Raymond Hettinger:
# * Thinking about Concurrency, Raymond Hettinger, Python core
#   developer (https://www.youtube.com/watch?v=Bv25Dwe84g0)
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
from multiprocessing import Process

def dispatcher(flist):
    dprocs = []
    for fnum in flist:
        p = Process(target=fib, args=(fnum,))
        dprocs.append(p)
        p.start()
    # Wait for all threads to finish
    for p in dprocs:
        p.join()

def main():
    myfibs = [36, 36, 36, 36]
    start = time.time()
    dispatcher(myfibs)
    end = time.time()
    print('Ellapsed time:  {}'.format(end - start))

# Must have/use for multi-processing or fails
if __name__ == '__main__':
    main()

