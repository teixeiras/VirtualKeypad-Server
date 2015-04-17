import ConfigParser
import os

from pipplware.pipLog import pipLog

class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

# Open child processes via os.system(), popen() or fork() and execv()
class pipConfig(object):

    """:type: string"""
    SECTION_MODULES = "Modules"

    """@type: string"""
    SECTION_NETWORK_SETTINGS = "Network"

    """:type: string"""
    SECTION_AUTHENTICATION = "Authtentication"

    """:type: string"""
    SECTION_INPUT = "Input"

    """:type: pipConfig"""
    config = ""


    @ClassProperty
    @classmethod
    def sharedInstance(cls):
        return pipConfig.config

    def __init__(self):
        self.configFile = ""
        if os.environ.has_key('PIPPLWARE_CONFIG'):
            self.configFile = os.environ['PIPPLWARE_CONFIG']

        pipConfig.config = ConfigParser.ConfigParser()
        if (len(self.configFile) == 0) :
            self.configFile = "/etc/pipplware/daemon.cfg"

        if os.path.isfile(self.configFile):
            pipLog.sharedInstance.debug("Using config file " + self.configFile)
            pipConfig.config.read(self.configFile)


    def get(self, section, item):
        if self[item]:
            return self[item]
        return pipConfig.config.get(section, item, 0)

    def getboolean(self, section, item):
        if self[item]:
            return self[item]
        return pipConfig.config.getboolean(section, item, 0)

    def save(self):
        with open(self.configFile, 'wb') as configfile:
            pipConfig.config.write(configfile)