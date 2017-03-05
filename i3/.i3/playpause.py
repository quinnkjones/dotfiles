#!/usr/bin/python
import websocket
import thread
import socket
import asyncore
import json
import os
import threading

SOCKET_FILE = '/tmp/googleplaystate'
TOKEN = '4d61a9f0-c127-4e1e-9ecc-2202d90ba883'

class GPMDP_Client(asyncore.dispatcher):



    def on_GPDMP_Message(self,ws,message):
        pass

    def on_GPDMP_Error(self,ws,error):
        print error

    def on_GPDMP_Close(self,ws):
        self.playing = False
        #set ws to reopen

    def on_GPDMP_Open(self,ws):
        p = json.dumps({'namespace':'connect','method':'connect','arguments':['i3server',TOKEN]})
        self.ws.send(p)


    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.ws = websocket.WebSocketApp('ws://localhost:5672',
                                         on_message = self.on_GPDMP_Message,
                                         on_error = self.on_GPDMP_Error,
                                         on_close = self.on_GPDMP_Close)
        self.ws.on_open = self.on_GPDMP_Open
        t = threading.Thread(target=self.ws.run_forever)
        t.start()



        self.create_socket(socket.AF_INET,
                           socket.SOCK_STREAM)
        self.bind(('127.0.0.1',6666))
        self.listen(1)

    def togglePlayPause(self):
        d = {
            "namespace":"playback",
            "method":"playPause",
        }
        pay = json.dumps(d)

        self.ws.send(pay)

    def next(self):
        d = {
            "namespace":"playback",
            "method":"forward"
        }
        self.ws.send(json.dumps(d))

    def prev(self):
        d = {
            "namespace":"playback",
            "method":"rewind"
        }
        self.ws.send(json.dumps(d))

    def handle_accept(self):
        pair = self.accept()

        if pair is not None:
            sock,addr = pair
            mesg = sock.recv(6)

            if mesg.strip() == 'toggle':
                self.togglePlayPause()
            elif mesg.strip() == 'back':
                self.prev()
            else:
                self.next()




if __name__ == "__main__":
    import sys
    if len(sys.argv) != 1:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(('127.0.0.1',6666))
        if sys.argv[1] == 't':
            client.send(b'toggle')
        elif sys.argv[1] == 'p':
            client.send(b'back')
        else:
            client.send(b'skip')
        client.close()
    else:
        serve = GPMDP_Client()
        asyncore.loop()


