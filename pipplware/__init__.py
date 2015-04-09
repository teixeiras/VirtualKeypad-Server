import threading, logging, os, time, sys, traceback

from pipInput import pipInput
import pipServices

from pipplware.pipConfig import pipConfig
from pipCec import pipCec
from pipplware.pipBonjour import pipBonjour
from pipplware.web import pipWebServer

pipInputObject = pipInput.pipInput()
pipConfig = pipConfig()


name =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"name")
regtype =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"regtype")
port =  int(pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"port"))

if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "bonjour")):
    bonjour = pipBonjour(name, regtype, port)
    thread = threading.Thread(target = bonjour.start_module)
    thread.start()

if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "cec")):
    pipcec = pipCec(pipInputObject)
    thread = threading.Thread(target = pipcec.start_module)
    thread.start()


if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "webservice")):
    webserver = pipWebServer.pipWebServer(port)
    webserver.start_module()
