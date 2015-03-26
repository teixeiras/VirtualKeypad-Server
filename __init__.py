import threading, os, time,  sys, traceback
from pipConfig import pipConfig
from pipInput import pipInput


pipInputObject = pipInput()
pipConfig = pipConfig()


name =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"name")
regtype =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"regtype")
port =  int(pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"port"))

if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "bonjour")):
    import pipBonjour
    bonjour = pipBonjour.pipBonjour(name, regtype, port)
    thread = threading.Thread(target = bonjour.startModule)
    thread.start()


if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "webservice")):
    try:
        from web import pipWebServer
        webserver = pipWebServer.pipWebServer(port)
        thread = threading.Thread(target = webserver.startModule)
        thread.start()
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60



if bool(pipConfig.sharedInstance.get(pipConfig.SECTION_MODULES, "cec")):
    import pipCec
    cec = pipCec.pipCec(pipInputObject)
    thread = threading.Thread(target = cec.startModule)
    thread.start()


try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print "Received an kill signal"
    os._exit(1)
