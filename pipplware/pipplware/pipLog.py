import syslog

class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class pipLog(object):

    """:type: pipLog"""
    log = ""


    @ClassProperty
    @classmethod
    def sharedInstance(cls):
        return pipLog.log

    def __init__(self):
        pipLog.log = self

    def debug(self, message):
        syslog.syslog(syslog.LOG_DEBUG, message)
        print message
