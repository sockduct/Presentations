# Asynchronous fibonacci server - asyncsrv.py
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
from fib import fib
import asyncio

# Define asynchronous function
async def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    # Must make socket non-blocking
    sock.setblocking(False)
    while True:
        # Use sock_accept from asyncio library
        # * Must "asynchronously wait" for it as it blocks (and async function)
        client, addr = await loop.sock_accept(sock)
        print('Connection from', addr)
        loop.create_task(fib_handler(client))

async def fib_handler(client):
    with client:
        while True:
            req = await loop.sock_recv(client, 100)
            if not req:
                break
            n = int(req)
            result = fib(n)
            resp = str(result).encode('ascii') + b'\n'
            # Note - no asynchronous sock_send, only sock_sendall
            await loop.sock_sendall(client, resp)
    print('Connection closed')

# Create "handle" to event loop
loop = asyncio.get_event_loop()
# Create running instance of fib_server
loop.create_task(fib_server(('', 25000)))
# Start event loop
loop.run_forever()

