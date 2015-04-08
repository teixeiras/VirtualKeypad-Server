import logging, json, websocket, threading

from pipplware.pipInput import pipInput
from pipplware.piSession import piSession
from pipplware.pipConfig import pipConfig

from websocket import WebsocketServer

clients = [None, None, None, None]


def clientNumber(client):
    for (i, client_object) in enumerate(clients):

        if client == client_object:
            return i


# Called for every client connecting (after handshake)
def new_client(client, server):
    for (i, client) in enumerate(clients):

        if client == None:
            clients[i] = client

            break


# Called for every client disconnecting
def client_left(client, server):
    print("Close connection")
    for (i, client_object) in enumerate(clients):

        if client == client_object:
            clients[i] = None


# Called when a client sends a message
def message_received(client, server, message):
    data = json.loads(message)

    print("Got message: %s" % json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

    if data["action"] == "key":
        pipInput.pipInput.sharedInstance.sendKeyUsingKeyCode(data["content"]["key"])

    if data["action"] == "session":
        session = piSession(client, data["content"]["token"])

        session.input = clientNumber()

        session.send("WELCOME %s" % session.token)


class piSocket(object):
    def start_module(self):
        websocketPort = pipConfig.sharedInstance.get(pipConfig.SECTION_INPUT, "websocket_port")

        server = WebsocketServer(int(websocketPort), "0.0.0.0")

        server.set_fn_new_client(new_client)

        server.set_fn_client_left(client_left)

        server.set_fn_message_received(message_received)

        server.run_forever()