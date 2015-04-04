from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import urlparse
import subprocess
import imp

import pipPSUtil

# Modules dependencies
import pipInput
import pipTransmission

try:
    imp.find_module('psutil')
except ImportError:
    print "You need to install psutil modules"
    print "sudo pip install psutil"
    print "No pip? sudo apt-get install build-essential python-dev python-pip"

util = pipPSUtil.pipPSUtil()
transmission = pipTransmission.pipTransmission()


class Request(object):
    def __init__(self, url, handler):
        self.url = url
        self.handler = handler

    def execute(self, arguments):
        print "Not defined"


    def sendSuccess(self):
        self.sendMessage({"status": "1"})

    def sendError(self, message):
        self.sendMessage({"status": "0", "statusMessage": message})

    def sendMessage(self, message):
        self.handler.send_response(200)
        self.handler.send_header('Content-type', 'text/html')
        self.handler.end_headers()
        self.handler.wfile.write(message)


class RebootCmdRequest(Request):
    def __init__(self, handler):
        super(RebootCmdRequest, self).__init__("/mode/reboot", handler)

    def execute(self, arguments):
        subprocess.call(['sudo', 'reboot'])
        self.sendSuccess


class BothCmdRequest(Request):
    def __init__(self, handler):
        super(BothCmdRequest, self).__init__("mode/both", handler)

    def execute(self, arguments):
        subprocess.call(['sudo', '/usr/local/bin/boottoes_kodi'])
        self.sendSuccess


class EmulationCmdRequest(Request):
    def __init__(self, handler):
        super(EmulationCmdRequest, self).__init__("/mode/emulation", handler)

    def execute(self, arguments):
        subprocess.call(['sudo', '/usr/local/bin/boottoes'])
        self.sendSuccess


class KodiCmdRequest(Request):
    def __init__(self, handler):
        super(KodiCmdRequest, self).__init__("/mode/kodi", handler)

    def execute(self, arguments):
        subprocess.call(['sudo', '/usr/local/bin/boottokodi'])
        self.sendSuccess


class XFCECmdRequest(Request):
    def __init__(self, handler):
        super(XFCECmdRequest, self).__init__("/mode/xfce", handler)

    def execute(self, arguments):
        subprocess.call(['sudo', '/usr/local/bin/boottoxfce'])
        self.sendSuccess


class TerminalCmdRequest(Request):
    def __init__(self, handler):
        super(TerminalCmdRequest, self).__init__("/mode/terminal", handler)

    def execute(self, arguments):
        subprocess.call(['sudo', '/usr/local/bin/boottoterminal'])
        self.sendSuccess


class InfoRequest(Request):
    def __init__(self, handler):
        super(InfoRequest, self).__init__("/info", handler)

    def execute(self, arguments):
        self.sendMessage(util.output())


class KillProcessRequest(Request):
    def __init__(self, handler):
        super(KillProcessRequest, self).__init__("/kill_process", handler)

    def execute(self, arguments):
        self.sendMessage(util.kill_process(arguments['pid']))


class TransmissionRequest(Request):
    def __init__(self, handler):
        super(TransmissionRequest, self).__init__("/transmission", handler)

    def execute(self, arguments):
        self.sendMessage(transmission.output())


class TransmissionAddRequest(Request):
    def __init__(self, handler):
        super(TransmissionAddRequest, self).__init__("/transmission_add", handler)

    def execute(self, arguments):
        print "Add torrent"

        uri = ""
        if 'uri' in arguments.keys():
            uri = arguments['uri'][0]

        if len(uri) == 0:
            self.sendError("Missing arguments")
            return

        print  "The url to be added" + uri

        self.sendMessage(transmission.add(uri))


class KeyRequest(Request):
    def __init__(self, handler):
        super(KeyRequest, self).__init__("/key", handler)

    def execute(self, arguments):
        print arguments
        print  "The key is " + arguments["key"]
        pipInput.pipInput.sharedInstance.sendKeyUsingKeyCode(arguments["key"])
        self.sendSuccess


class Handler(BaseHTTPRequestHandler):

    def route(self, path, arguments):
        if not hasattr(self, 'requests'):
            self.requests = []
            self.requests.append(RebootCmdRequest(self))
            self.requests.append(BothCmdRequest(self))
            self.requests.append(EmulationCmdRequest(self))
            self.requests.append(KodiCmdRequest(self))
            self.requests.append(XFCECmdRequest(self))
            self.requests.append(TerminalCmdRequest(self))

            self.requests.append(InfoRequest(self))
            self.requests.append(KillProcessRequest(self))

            self.requests.append(TransmissionRequest(self))
            self.requests.append(TransmissionAddRequest(self))

            self.requests.append(KeyRequest(self))

        for requestHandler in self.requests:
            if requestHandler.url == path:
                requestHandler.execute(arguments)


    def do_GET(self):
        qs = {}
        path = self.path
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)

        self.route(path, qs)


    def do_POST(self):

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
            })

        fields = {}
        path = self.path

        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = {}
            qs = urlparse.parse_qs(tmp)
            fields.update(qs)

        for key in form.keys():
            fields[key] = form.getvalue(key)

        self.route(path, fields)

        return


class pipWebServer(object):
    def __init__(self, port):
        print "Webservice at port: " + str(port)
        self.httpd = HTTPServer(('0.0.0.0', port), Handler)


    def startModule(self):
        self.httpd.serve_forever()