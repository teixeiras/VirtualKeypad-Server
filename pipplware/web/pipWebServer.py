import subprocess
import imp, json
from pipInput import pipInput
from bottle import request, run, post, get, auth_basic
from pipplware.pipConfig import pipConfig
import pipPSUtil
from pipplware.piSession.piSession import piSession

# Modules dependencies
import pipTransmission

try:
    imp.find_module('psutil')
except ImportError:
    print "You need to install psutil modules"
    print "sudo pip install psutil"
    print "No pip? sudo apt-get install build-essential python-dev python-pip"


def sendSuccess():
    return sendMessage({"status": "1"})

def sendError(message):
    return sendMessage({"status": "0", "statusMessage": message})

def sendMessage( message):
    return message


def check_pass(username, password):
    usernameConfig = "pippplware"
    passwordConfig = pipConfig.sharedInstance.get(pipConfig.SECTION_AUTHENTICATION, "password")

    if username == usernameConfig and password == passwordConfig:
        return True
    return False

@get("/mode/reboot")
@post("/mode/reboot")
@auth_basic(check_pass)
def RebootCmdRequest():
    subprocess.call(['sudo', 'reboot'])
    return sendSuccess

@get("mode/both")
@post("mode/both")
@auth_basic(check_pass)
def BothCmdRequest():
    subprocess.call(['sudo', '/usr/local/bin/boottoes_kodi'])
    return sendSuccess

@get("/mode/emulation")
@post("/mode/emulation")
@auth_basic(check_pass)
def EmulationCmdRequest():
    subprocess.call(['sudo', '/usr/local/bin/boottoes'])
    return sendSuccess

@get("/mode/kodi")
@post("/mode/kodi")
@auth_basic(check_pass)
def KodiCmdRequest():
    subprocess.call(['sudo', '/usr/local/bin/boottokodi'])
    return sendSuccess

@get("/mode/xfce")
@post("/mode/xfce")
@auth_basic(check_pass)
def XFCECmdRequest():
    subprocess.call(['sudo', '/usr/local/bin/boottoxfce'])
    return sendSuccess


@get("/mode/terminal")
@post("/mode/terminal")
@auth_basic(check_pass)
def TerminalCmdRequest(self):
    subprocess.call(['sudo', '/usr/local/bin/boottoterminal'])
    return self.sendSuccess

util = pipPSUtil.pipPSUtil()

@post("/info")
@get("/info")
@auth_basic(check_pass)
def InfoRequest():

    websocketPort = pipConfig.sharedInstance.get(pipConfig.SECTION_INPUT, "websocket_port")

    output = {"websocket_port": websocketPort,
              "bonjour_actice": bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "bonjour")),
              "webservice_actice": bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "webservice")),
              "pipCec_actice": bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "pipCec")),
              "websocketserver_actice": bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "websocketserver")),
              "token":piSession.generateToken()
    }

    return sendMessage(json.dumps(output))


@post("/stats")
@get("/stats")
@auth_basic(check_pass)
def InfoRequest():
    return sendMessage(util.output())

@post("/kill_process")
@auth_basic(check_pass)
def KillProcessRequest():
    return sendMessage(util.kill_process(request.forms.get('pid')))


transmission = pipTransmission.pipTransmission()
@get("/transmission")
@post("/transmission")
@auth_basic(check_pass)
def TransmissionRequest():
    return sendMessage(transmission.output())


@post("/transmission_add")
@auth_basic(check_pass)
def TransmissionAddRequest():
    print "Add torrent"

    uri = request.forms.get('uri')

    if len(uri) == 0:
        sendError("Missing arguments")
        return
    print  "The url to be added" + uri
    return sendMessage(transmission.add(uri))

@post("/transmission_add_file")
@auth_basic(check_pass)
def TransmissionAddRequest():
    print "Add torrent by file"

    file = request.forms.get('file')
    if len(file) == 0:
        sendError("Missing arguments")
        return

    fh = open("/tmp/file.torrent", "wb")
    fh.write(file.decode('base64'))
    fh.close()

    return sendMessage(transmission.addFile("/tmp/file.torrent"))

@get("/key")
@post("/key")
@auth_basic(check_pass)
def KeyRequest():
    print  "The key is " + request.forms.get('key')
    pipInput.pipInput.sharedInstance.sendKeyUsingKeyCode(request.forms.get('key'))
    return sendSuccess


class pipWebServer(object):
    def __init__(self, port):
        self.port = port

    def startModule(self):
        print "Webservice at port: " + str(self.port)
        run(host='0.0.0.0', port=self.port, debug=True)
