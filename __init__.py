import threading, os, time, imp

import pipBonjour
import pipInput
import pipCec
from web import pipWebServer


name    = "virtualKeypad"
regtype = "_virtualKeypad._tcp"
port    = 1134

#Modules dependencies
try:
    imp.find_module('psutil')
except ImportError:
    print "You need to install psutil modules"
    print "sudo pip install psutil"
    print "No pip? sudo apt-get install build-essential python-dev python-pip"


pipInputObject = pipInput.pipInput()

bonjour = pipBonjour.pipBonjour(name, regtype, port)
thread = threading.Thread(target = bonjour.startModule)
thread.start()


webserver = pipWebServer.pipWebServer(port)
thread = threading.Thread(target = webserver.startModule)
thread.start()

cec = pipCec.pipCec(pipInputObject)
thread = threading.Thread(target = cec.startModule)
thread.start()
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print "Received an kill signal"
    os._exit(1)
