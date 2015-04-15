from pipplware.pipInput import pipInput

def main():
    import threading

    import pipServices
    from pipplware.pipConfig import pipConfig
    import pipCec
    from pipplware.pipBonjour import pipBonjour
    from pipplware.web import pipWebServer

    pipInputObject = pipInput.pipInput()
    pipConfig = pipConfig()


    name =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"name")
    regtype =  pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"regtype")
    port =  int(pipConfig.sharedInstance.get(pipConfig.SECTION_NETWORK_SETTINGS,"port"))

    if pipConfig.sharedInstance.getboolean(pipConfig.SECTION_MODULES, "bonjour"):
        bonjour = pipBonjour(name, regtype, port)
        thread = threading.Thread(target = bonjour.start_module)
        thread.start()

    if pipConfig.sharedInstance.getboolean(pipConfig.SECTION_MODULES, "cec"):
        cec = pipCec.pipCec(pipInputObject)
        thread = threading.Thread(target = cec.start_module)
        thread.start()


    if pipConfig.sharedInstance.getboolean(pipConfig.SECTION_MODULES, "webservice"):
        webserver = pipWebServer.pipWebServer(port)
        webserver.start_module()


if __name__ == '__main__':
    main()
