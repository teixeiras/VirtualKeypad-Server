import uinput
class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class pipInput(object):
    instance = ""
    @ClassProperty
    @classmethod
    def sharedInstance(cls):
        return pipInput.instance

    def __init__(self):
        pipInput.instance = self
        self.device = uinput.Device([uinput.KEY_UP,
            uinput.KEY_LEFT,
			uinput.KEY_RIGHT,
			uinput.KEY_DOWN,
			uinput.KEY_ENTER,
			uinput.KEY_BACKSPACE,
			uinput.KEY_RIGHTSHIFT, uinput.KEY_RIGHTCTRL, 
			uinput.KEY_PAGEUP, uinput.KEY_PAGEDOWN])

    def sendKeyUsingEvent(self, event):
        self.device.emit_click(event)

    def sendKeyUsingKeyCode(self, keyCode):
        print "key "+keyCode+ " will be sent"
        self.device.emit_click([0x01, int(keyCode)])
