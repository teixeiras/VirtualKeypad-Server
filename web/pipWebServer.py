from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi, pipInput, pipPSUtil, pipTransmission, urlparse,subprocess

def sendSuccess(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write({"status":"1"})

class handler(BaseHTTPRequestHandler):
    util =  pipPSUtil.pipPSUtil()
    transmission = pipTransmission.pipTransmission()

    def bootRequest(self, path, arguments):
        if path == "/mode/reboot":
            subprocess.call(['sudo', 'reboot'])
            sendSuccess

        if path == "/mode/both":
            subprocess.call(['sudo', '/usr/local/bin/boottoes_kodi'])
            sendSuccess

        if path == "/mode/emulation":
            subprocess.call(['sudo', '/usr/local/bin/boottoes'])
            sendSuccess

        if path == "/mode/kodi":
            subprocess.call(['sudo', '/usr/local/bin/boottokodi'])
            sendSuccess

        if path == "/mode/xfce":
            subprocess.call(['sudo', '/usr/local/bin/boottoxfce'])
            sendSuccess

        if path == "/mode/terminal":
            subprocess.call(['sudo', '/usr/local/bin/boottoterminal'])
            sendSuccess

    def infoRequest(self, path, arguments):
        if path == "/info":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(handler.util.output())


    def transmissionRequest(self, path, arguments):
        if path == "/transmission":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(handler.transmission.output())

        print path
        if path == "/transmission_add":
            print "Add torrent"

            uri = ""
            if 'uri' in arguments.keys():
                uri = arguments['uri'][0]


            if len(uri) == 0:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                return

            print  "The url to be added" + uri


            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(handler.transmission.add(uri))


    def keyRequest(self, path, arguments):
        if path=="/key":
            print arguments
            print  "The key is " + arguments["key"]
            pipInput.pipInput.sharedInstance.sendKeyUsingKeyCode(arguments["key"])
            sendSuccess

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
                environ={'CONTENT_TYPE':self.headers['Content-Type'],
            })

        qs = {}
        path = self.path

        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            form.update(qs)


        self.keyRequest(path, form)
        self.infoRequest(path, form)
        self.transmissionRequest(path, form)
        self.bootRequest(path, form)
        return

class pipWebServer(object):

    def __init__(self, port):
        print "Webservice at port: " + str(port)
        self.httpd = HTTPServer(('0.0.0.0', port), handler)


    def startModule(self):
        self.httpd.serve_forever()