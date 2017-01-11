#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 7 - server_simple.py
# Simple server that only serves one client at a time; others have to wait.

import random
import select
import socket
import sys
import Queue

ICONNS = 6  # Inbound client connection queue
PORT = 1060
qa = (('What is your name?', 'My name is Sir Lancelot of Camelot.'),
      ('What is your quest?', 'To seek the Holy Grail.'),
      ('What is your favorite color?', 'Blue.'))
qadict = dict(qa)
randans = ("I'm not sure.","That's a lame question.",
            "I don't understand what you're asking.","You're crazy.",
            "Go away.","Your mother is a hamster.")
# Select lists
inputs = []
outputs = []
# no separate error list
timeout = 60

# Queue
messageiq = {}
messageoq = {}

def reply(question):
    if question in qadict:
        answer = qadict[question]
    else:
        raindex = random.randint(0,len(randans)-1)
        answer = randans[raindex]
    return answer

def setup():
    if len(sys.argv) != 2:
        print >>sys.stderr, 'usage: %s interface' % sys.argv[0]
        exit(2)
    interface = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)
    sock.bind((interface, PORT))
    sock.listen(ICONNS)
    print 'Ready and listening at %r port %d' % (interface, PORT)
    return sock

def server_loop(listen_sock):
    while inputs:
        print '\nWaiting for next event...'
        #print 'Select Read List:  ' + str(inputs)
        #print 'Select Write List:  ' + str(outputs)
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
        if not (readable or writable or exceptional):
            print 'Select timeout expired (' + str(timeout) + ' seconds)...'
            continue
        # input
        for s in readable:
            if s is listen_sock:  # Main socket listening for inbound clients
                clientsock, clientaddr = s.accept()
                clientaddr = clientaddr[0] + ':' + str(clientaddr[1])
                print 'Accepted connection from ' + clientaddr
                clientsock.setblocking(False)
                inputs.append(clientsock)
                #messageiq[clientsock] = Queue.Queue()
                messageoq[clientsock] = Queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    # inbound client data
                    # Complete question
                    # Sloppy - might not get entire question on one recv call
                    if data.endswith('?'):
                        answer = reply(data)
                    # Incomplete question, queue...
                    #else:
                    #    messageiq[s].put(data)
                    print 'Received "' + data + '" from ' + str(s.getpeername())
                    messageoq[s].put(answer)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # empty client connection = close connection
                    print 'End of Transmission from ' + str(s.getpeername())
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close
                    del messageoq[s]
        # output
        for s in writable:
            try:
                nextmsg = messageoq[s].get_nowait()
            except Queue.Empty:
                print 'Output queue for ' + str(s.getpeername()) + ' is empty'
                outputs.remove(s)
            except KeyError:
                print 'Attempt to write to closed socket - continuing'
            else:
                print 'Sending "' + nextmsg + '" to ' + str(s.getpeername())
                # Sloppy - possible that not everything can be sent at onece...
                s.send(nextmsg)
        # exceptions
        for s in exceptional:
            print 'Exception occurred for ' + str(s.getpeername())
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del messageoq[s]

if __name__ == '__main__':
    listen_sock = setup()
    inputs.append(listen_sock)
    server_loop(listen_sock)

