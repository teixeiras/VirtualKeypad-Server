__author__ = 'teixeiras'
import os
import binascii

class piSession(object):
    clients = []
    websocket = None
    token = None

    def __init__(self, websocket, token):
        self.token = token
        self.websocket = websocket
        Client.append(self)

    def validate(self):
        if self.websocket.running == False:
            print "The socket is dead dude!"

    @staticmethod
    def clientByWebsocket(websocket):
        for (i, client) in enumerate(Client.clients):

            if client.websocket == websocket:

               return client

        return None

    @staticmethod
    def clientByToken(token):
        for (i, client) in enumerate(Client.clients):

            if client.token == token:

               return client

        return None

    @staticmethod
    def generateToken():
        return binascii.hexlify(os.random(16))