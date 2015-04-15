VERSION = (0, 9, 3, 'final', 0)

__all__ = [
    'WebSocketApplication',
    'Resource',
    'WebSocketServer',
    'WebSocketError',
    'get_version'
]


def get_version(*args, **kwargs):
    from .pipplware.web.bottle_websocket.geventwebsocket.utils import get_version
    return get_version(*args, **kwargs)

try:
    from .pipplware.web.bottle_websocket.geventwebsocket.resource import WebSocketApplication, Resource
    from .pipplware.web.bottle_websocket.geventwebsocket.server import WebSocketServer
    from .pipplware.web.bottle_websocket.geventwebsocket.exceptions import WebSocketError
except ImportError:
    pass
