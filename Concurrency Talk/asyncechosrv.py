# Simple, asyncio/event loop echo server
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
import asyncio

# Define asynchronous function
async def echo_server(address):
    # Create a socket, type IPv4, TCP
    sock = socket(AF_INET, SOCK_STREAM)
    # Set socket options
    # * Allow binding to address even if in use (also
    #   bypass TIME_WAIT delay)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # Bind socket to passed address, port tuple
    sock.bind(address)
    # Listen for incoming connections
    # * Use a queue that can hold up to 5 pending
    #   connections
    sock.listen(5)
    # Must make socket non-blocking
    sock.setblocking(False)
    while True:
        # Use sock_accept from asyncio library
        # * Must "asynchronously wait" for it as it
        #   blocks (and async function)
        client, addr = await loop.sock_accept(sock)
        loop.create_task(echo_handler(client, addr))

async def echo_handler(client, addr):
    print('Connection from {}'.format(addr))
    # Use context manager for socket "client":
    with client:
        # While not EOF (more data possible), loop
        while True:
            # Receive available data transmitted from
            # client
            data = await loop.sock_recv(client, 10000)
            # If no more data (EOF/EOT), break out of
            # loop
            if not data:
                break
            # Format data string
            data = 'Received:  '.encode('ascii') + data
            # Echo back to client
            await loop.sock_sendall(client, data)
    print('Connection from {} closed'.format(addr))

# Create "handle" to event loop
loop = asyncio.get_event_loop()
# Create running instance of fib_server
loop.create_task(fib_server(('', 25000)))
# Start event loop
loop.run_forever()

