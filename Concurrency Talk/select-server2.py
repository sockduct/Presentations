# Using example from pymotw.com/2/select/

# Imports
import select
import socket
import sys
import Queue

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

# Select can monitor 3 or 4 channels:
# Objects with data to be read, Objects ready to receive data,
# Objects with an error condition (usually a combination of input/output objects)
# Optionally a timeout - return if no input/output/error events during specified period
#
# Select - Sockets from which we expect to read
inputs = [ server ]

# Select - Sockets to which we expect to write
outputs = [ ]

# Select - Sockets to monitor for errors
# In this case just using inputs
# Same socket (input/output) so might be OK - not sure

# Select - Timeout period in seconds
timeout = 60

# This server waits for a socket to become writable before sending any data
# (instead of immediately sending the reply), each output connection uses a
# queue to act as a buffer for the data to be sent:
# Outgoing message queues (socket:Queue)
message_queues = {}

# Notes on select:
# select() returns three new lists, containing subsets of the contents of the lists
# passed in. All of the sockets in the readable list have incoming data buffered and
# available to be read. All of the sockets in the writable list have free space in
# their buffer and can be written to. The sockets returned in exceptional have had
# an error (the actual definition of "exceptional condition" depends on the platform).
#
# The "readable" sockets represent three possible cases. If the socket is the main
# "server" socket, the one being used to listen for connections, then the "readable"
# condition means it is ready to accept another incoming connection. In addition to
# adding the new connection to the list of inputs to monitor, this section sets the
# client socket to not block.
#
while inputs:
    # Wait for at least one of the sockets to be ready for processing
    print >>sys.stderr, '\nwaiting for the next event'
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
    #
    if not (readable or writable or exceptional):
        # Perform other work or end or whatever if select timeout expires
        print >>sys.stderr, 'Select timeout expired (' + str(timeout) + ' seconds)...'
        continue
    #
    # Handle inputs
    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            print >>sys.stderr, 'new connection from', client_address
            connection.setblocking(0)
            inputs.append(connection)
            #
            # Give the connection a queue for data we want to send
            message_queues[connection] = Queue.Queue()
        else:
            # This is sloppy - recv may return less than 1024 byte
            # Really need to loop for data and look for end of message
            # signal - but that's a lot more work...
            data = s.recv(1024)
            if data:
                # A readable client socket has data
                print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
                message_queues[s].put(data)
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)
            else:
                # Interpret empty result as closed connection
                print >>sys.stderr, 'closing', client_address, 'after reading no data'
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]
    #
    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            # No messages waiting so stop checking for writability.
            print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
            outputs.remove(s)
        else:
            print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
            # This is sloppy - send may not be able to transmit the entire
            # message, for that sendall should be used.  Should loop until
            # confirmed all data sent.
            s.send(next_msg)
    #
    # Handle "exceptional conditions"
    for s in exceptional:
        print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]

