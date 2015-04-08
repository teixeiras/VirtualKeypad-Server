import threading, logging, os, time, sys, traceback

from pipInput import pipInput
import pipServices

from pipplware.pipConfig import pipConfig
from pipCec import pipCec
import pipplware.pipBonjour
from pipplware.web import pipWebServer

from pipplware.piSocket import piSocket

pipInputObject = pipInput()
pipConfig = pipConfig()


name =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"name")
regtype =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"regtype")
port =  int(pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"port"))

if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "bonjour")):
    bonjour = pipBonjour.pipBonjour(name, regtype, port)
    thread = threading.Thread(target = bonjour.start_module)
    thread.start()

if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "websocketserver")):
    server = piSocket()
    thread = threading.Thread(target = server.start_module)
    thread.start()
"""
if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "cec")):
    pipcec = pipCec(pipInputObject)
    thread = threading.Thread(target = pipcec.start_module)
    thread.start()
"""

if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "webservice")):
    try:
        webserver = pipWebServer.pipWebServer(port)
        webserver.start_module()

    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60


try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print "Received an kill signal"
    os._exit(1)
