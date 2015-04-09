from pipplware.web.bottle import ServerAdapter
from gevent import pywsgi
from pipplware.web.bottle_websocket.geventwebsocket.handler import WebSocketHandler

class GeventWebSocketServer(ServerAdapter):
    def run(self, handler):
        pywsgi.WSGIServer((self.host, self.port), handler, handler_class=WebSocketHandler).serve_forever()
