import threading
import os
import time
import sys
import traceback

from pipplware.pipConfig import pipConfig
from pipplware.pipInput import pipInput
import pipplware.pipCec, pipplware.pipBonjour
from pipplware.web import pipWebServer

pipInputObject = pipInput()
pipConfig = pipConfig()


name =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"name")
regtype =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"regtype")
port =  int(pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"port"))

if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "bonjour")):
    bonjour = pipBonjour.pipBonjour(name, regtype, port)
    thread = threading.Thread(target = bonjour.startModule)
    thread.start()


if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "webservice")):
    try:
        webserver = pipWebServer.pipWebServer(port)
        webserver.startModule()

    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60



if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "cec")):
    cec = pipCec.pipCec(pipInputObject)
    thread = threading.Thread(target = cec.startModule)
    thread.start()


try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print "Received an kill signal"
    os._exit(1)
