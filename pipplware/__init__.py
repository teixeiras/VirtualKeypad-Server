import threading

import pipServices
from pipplware.pipCec import pipCec
from pipplware.pipConfig import pipConfig
from pipplware.pipBonjour import pipBonjour
from pipplware.pipInput import pipInput
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
    cec = pipCec(pipInputObject)
    thread = threading.Thread(target = cec.start_module)
    thread.start()


if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "webservice")):
    webserver = pipWebServer.pipWebServer(port)
    webserver.start_module()
