import logging, json, websocket, threading

from pipplware.pipConfig import pipConfig
from pipplware.pipInput import  pipInput
from pipplware.piSession import piSession

class WebSocketServer(websocket.WebSocket):

    clients = list(None,None,None,None)

    def __init__(self, client, server):

        super(WebSocketServer, self).__init__(client, server)

        for (i, client) in enumerate(WebSocketServer.clients):

            if client == None:

                WebSocketServer.clients[i] = self

                break


    def onmessage(self, data):

        super(WebSocketServer, self).onmessage(data)

        data = json.loads(data)

        logging.info("Got message: %s" % json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

        if data["action"] == "key":

            pipInput.pipInput.sharedInstance.sendKeyUsingKeyCode(data["content"]["key"])


        if data["action"] == "session":

            self.session = piSession(self, data["content"]["token"])

            self.session.input = self.clientNumber()

            self.send("WELCOME %s" % self.session.token)


    def clientNumber(self):

        for (i, client) in enumerate(WebSocketServer.clients):

            if client == self:

                return i


    def close(self):

        logging.info("Close connection")

        super(WebSocketServer, self).close()

        for (i, client) in enumerate(WebSocketServer.clients):

            if client == self:

                WebSocketServer.clients[i] = None


	def startModule(self):
		logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

        websocketPort = pipConfig.sharedInstance.get(pipConfig.SECTION_INPUT, "websocket_port")

        logging.info("Opening websocket on: %s" % websocketPort)

        server = websocket.WebSocketServer("localhost", websocketPort, WebSocketServer)

        server_thread = threading.Thread(target=server.listen, args=[5])

        server_thread.start()

