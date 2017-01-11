# Benchmark 2 - measure reqs/sec
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
from socket import *
from threading import Thread
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25000))

n = 0

def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0

Thread(target=monitor).start()

while True:
    _ = sock.send(b'1')
    resp = sock.recv(100)
    n += 1

#
# My Results:
# Single-threaded   ~20,000/sec
# Multi-threaded    ~19,500/sec
# Multi-process     ~20,000/sec
# Asyncio           ~8,500/sec
#

