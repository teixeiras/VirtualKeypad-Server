from pipplware.pipInput import customInput
from pipplware.pipInput import keyMapAndroid


class ClassProperty(property):
        def __get__(self, cls, owner):
            return self.fget.__get__(None, owner)()


class pipInput(object):
    instance = ""
    gamepads = []
    mouse=""
    keyboard=""

    @ClassProperty
    @classmethod
    def sharedInstance(cls):
        return pipInput.instance

    def __init__(self):
        pipInput.instance = self
        keys = []
        for key in keyMapAndroid.keyMap:
            keys.append(keyMapAndroid.keyMap[key])

        self.keyboard = customInput.Device(keys, name="pipplware-keyboard")
        events = (
            customInput.REL_X,
            customInput.REL_Y,
            customInput.BTN_LEFT,
            customInput.BTN_RIGHT
        )
        self.mouse = customInput.Device(events, name="pipplware-mouse")

        gamepadKeys= [customInput.BTN_X,
                      customInput.BTN_Y,
                      customInput.BTN_Z,
                      customInput.BTN_A,
                      customInput.BTN_B,
                      customInput.BTN_C,
                      customInput.BTN_SELECT,
                      customInput.BTN_START,
                      customInput.ABS_X + (0, 255, 0, 0),
                      customInput.ABS_Y + (0, 255, 0, 0)]

        for i in range(0,3):
            self.gamepads.append(customInput.Device(gamepadKeys, name="pipplware_gamepad_"+str(i)))

    def sendKeyUsingEvent(self, event):
        self.keyboard.emit_click(event)

    def sendKeyUsingKeyCode(self, keyCode):
        print "key " + keyCode + " will be sent"
        self.keyboard.emit_click([0x01, int(keyCode)])

    def sendMultiKeyUsingKeyCode(self, keyCodes):
        combo = [];
        for key in keyCodes :
            combo.append([0x01, int(key)])
        self.keyboard.emit_combo(combo)


    def moveMouse(self, X, Y):
        print "Mouse moved"
        self.mouse.emit(customInput.REL_X, X, syn=False)
        self.mouse.emit(customInput.REL_Y, Y)

    def clickMouseLeft(self):
        print "Left mouse clicked"
        self.mouse.emit_click(customInput.BTN_LEFT)

    def clickMouseRight(self):
        print "Right mouse clicked"
        self.mouse.emit_click(customInput.BTN_RIGHT)


    def gamepadPressOn(self, joy, key):
        self.gamepads[joy].emit_click(key)
