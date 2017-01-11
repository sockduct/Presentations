# simple partial select example from myserver-select.py
# That example based on server_simple.py from
# Foundations of Python Network Programming, 2e, Ch 7
# https://www.safaribooksonline.com/library/view/foundations-of-python/9781430230038/
#
# Note:  This example is designed for Python 2.x
#
# For Python 3.x coverage, see 3e of book:
# https://www.safaribooksonline.com/library/view/foundations-of-python/9781430258551/
#
# Created for Concurrent Python presentation
#
# Based on examples/code from x
#
from socket import *
import select
from Queue import Queue

# Socket lists
inputs = []
outputs = []

# Queues
msg_in = {}
msg_out = {}

timeout = 60

# Setup server socket and put into my_sockets list above
# <Code omitted>

def server_loop(srv_sock):
    # While there are sockets in the list, process them
    while inputs:
        readable, writable, exceptional = select.select(
                inputs, outputs, inputs, timeout)
        if not (readable or writable or exceptional):
            # select tiemout expired, next iteration of
            # loop
            continue
        # input
        for s in readable:
            # Main socket listening for inbound clients
            if s is listen_sock:
                clientsock, clientaddr = s.accept()
                clientaddr = clientaddr[0] + ':' + str(
                        clientaddr[1])
                print 'Accepted connection from ' + \
                        clientaddr
                # Make socket non-blocking
                clientsock.setblocking(False)
                # Add to input socket list
                inputs.append(clientsock)
                msg_out[clientsock] = Queue()
            else:
                data = s.recv(1024)
                if data:
                    # inbound client data
                    # Sloppy - might not get entire
                    # question on one recv call
                    if data.endswith('?'):
                        answer = reply(data)
                    # Incomplete question, queue...
                    msg_out[s].put(answer)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # empty client connection = close
                    # connection
                    print 'End of Transmission from ' + \
                            str(s.getpeername())
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close
                    del messageoq[s]
        # output
        for s in writable:
            (...)

