from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import urlparse
import subprocess
import imp

import pipPSUtil





#Modules dependencies
from pipplware import pipInput
from pipplware.web import pipTransmission

try:
    imp.find_module('psutil')
except ImportError:
    print "You need to install psutil modules"
    print "sudo pip install psutil"
    print "No pip? sudo apt-get install build-essential python-dev python-pip"


class handler(BaseHTTPRequestHandler):
    util =  pipPSUtil.pipPSUtil()
    transmission = pipTransmission.pipTransmission()

    def bootRequest(self, path, arguments):
        if path == "/mode/reboot":
            subprocess.call(['sudo', 'reboot'])
            self.sendSuccess

        if path == "/mode/both":
            subprocess.call(['sudo', '/usr/local/bin/boottoes_kodi'])
            self.sendSuccess

        if path == "/mode/emulation":
            subprocess.call(['sudo', '/usr/local/bin/boottoes'])
            self.sendSuccess

        if path == "/mode/kodi":
            subprocess.call(['sudo', '/usr/local/bin/boottokodi'])
            self.sendSuccess

        if path == "/mode/xfce":
            subprocess.call(['sudo', '/usr/local/bin/boottoxfce'])
            self.sendSuccess

        if path == "/mode/terminal":
            subprocess.call(['sudo', '/usr/local/bin/boottoterminal'])
            self.sendSuccess

    def infoRequest(self, path, arguments):
        if path == "/info":
            self.sendMessage(handler.util.output())

        if path == "/kill_process":
            self.sendMessage(handler.util.kill_process(arguments['pid']))

    def transmissionRequest(self, path, arguments):
        if path == "/transmission":
            self.sendMessage(handler.transmission.output())

        print path
        if path == "/transmission_add":
            print "Add torrent"

            uri = ""
            if 'uri' in arguments.keys():
                uri = arguments['uri'][0]


            if len(uri) == 0:
                self.sendError("Missing arguments")
                return

            print  "The url to be added" + uri

            self.sendMessage(handler.transmission.add(uri))


    def keyRequest(self, path, arguments):
        if path=="/key":
            print arguments
            print  "The key is " + arguments["key"]
            pipInput.pipInput.sharedInstance.sendKeyUsingKeyCode(arguments["key"])
            self.sendSuccess



    def do_GET(self):
        qs = {}
        path = self.path
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)

        self.infoRequest(path, qs)
        self.transmissionRequest(path,  qs)
        self.bootRequest(path, qs)

    def do_POST(self):

        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                 environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
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

        self.keyRequest(path, fields)
        self.infoRequest(path, fields)
        self.transmissionRequest(path, fields)
        self.bootRequest(path, fields)
        return

    def sendSuccess(self):
        self.sendMessage({"status":"1"})

    def sendError(self, message):
        self.sendMessage({"status":"0", "statusMessage":message})

    def sendMessage(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(message)


class pipWebServer(object):

    def __init__(self, port):
        print "Webservice at port: " + str(port)
        self.httpd = HTTPServer(('0.0.0.0', port), handler)


    def startModule(self):
        self.httpd.serve_forever()