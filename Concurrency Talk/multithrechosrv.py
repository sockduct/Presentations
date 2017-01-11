# Simple, multi-threaded echo server
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

def echo_server(address):
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
    while True:
        # Get socket and address, port tuple of
        # connecting client
        client, addr = sock.accept()
        # Create new thread for handler dispatch
        Thread(target=echo_handler,
               args=(client,addr)).start()

def echo_handler(client, addr):
    print('Connection from {}'.format(addr))
    # Use context manager for socket "client":
    with client:
        # While not EOF (more data possible), loop
        while True:
            # Receive available data transmitted from
            # client
            data = client.recv(10000)
            # If no more data (EOF/EOT), break out of
            # loop
            if not data:
                break
            # Format data string
            data = 'Received:  '.encode('ascii') + data
            # Echo back to client
            client.sendall(data)
    print('Connection from {} closed'.format(addr))

# Start echo server on all available interfaces (with
# IPv4 addresses)
# * Use TCP port 25,000
echo_server(('', 25000))

