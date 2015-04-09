from sys import platform as _platform
class ClassProperty(property):
        def __get__(self, cls, owner):
            return self.fget.__get__(None, owner)()

if _platform == "darwin":
    class pipInput(object):
        instance = ""
        @ClassProperty
        @classmethod
        def sharedInstance(cls):
            return pipInput.instance

        def __init__(self):
            pipInput.instance = self
            print "Mac pipInput Constructor"

        def sendKeyUsingEvent(self, event):
            print "key "+ event + " will be sent"

        def sendKeyUsingKeyCode(self, keyCode):
            print "key "+ keyCode + " will be sent"


else:
    import customInput
    class pipInput(object):
        instance = ""
        @ClassProperty
        @classmethod
        def sharedInstance(cls):
            return pipInput.instance

        def __init__(self):
            pipInput.instance = self
            self.device = customInput.Device([customInput.KEY_UP,
                customInput.KEY_LEFT,
                customInput.KEY_RIGHT,
                customInput.KEY_DOWN,
                customInput.KEY_ENTER,
                customInput.KEY_BACKSPACE,
                customInput.KEY_RIGHTSHIFT, customInput.KEY_RIGHTCTRL,
                customInput.KEY_PAGEUP, customInput.KEY_PAGEDOWN])

        def sendKeyUsingEvent(self, event):
            self.device.emit_click(event)

        def sendKeyUsingKeyCode(self, keyCode):
            print "key "+keyCode+ " will be sent"
            self.device.emit_click([0x01, int(keyCode)])
