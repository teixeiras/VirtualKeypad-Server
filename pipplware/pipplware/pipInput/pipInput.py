from pipplware.pipInput import customInput
from pipplware.pipInput import keyMapAndroid


class ClassProperty(property):
        def __get__(self, cls, owner):
            return self.fget.__get__(None, owner)()


class pipInput(object):
    instance = ""
    gamepads = None
    mouse=None
    keyboard=None

    @ClassProperty
    @classmethod
    def sharedInstance(cls):
        return pipInput.instance

    def __init__(self):
        pipInput.instance = self


    def initKeyboard(self):
        keys = []
        for key in keyMapAndroid.keyMap:
            keys.append(keyMapAndroid.keyMap[key])

        self.keyboard = customInput.Device(keys, name="pipplware-keyboard")

    def initMouse(self):
        events = (
            customInput.REL_X,
            customInput.REL_Y,
            customInput.BTN_LEFT,
            customInput.BTN_RIGHT
        )
        self.mouse = customInput.Device(events, name="pipplware-mouse")

    def initGamepad(self):
        self.gamepads=[]
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
        if self.keyboard == None:
            self.initKeyboard()

        self.keyboard.emit_click(event)

    def sendKeyUsingKeyCode(self, keyCode):
        if self.keyboard == None:
            self.initKeyboard()

        print "key " + keyCode + " will be sent"
        self.keyboard.emit_click([0x01, int(keyCode)])

    def sendMultiKeyUsingKeyCode(self, keyCodes):
        if self.keyboard == None:
            self.initKeyboard()

        combo = [];
        for key in keyCodes :
            combo.append([0x01, int(key)])
        self.keyboard.emit_combo(combo)


    def moveMouse(self, X, Y):
        if self.mouse == None:
            self.initMouse()
        print "Mouse moved"
        self.mouse.emit(customInput.REL_X, X, syn=False)
        self.mouse.emit(customInput.REL_Y, Y)

    def clickMouseLeft(self):
        if self.mouse == None:
            self.initMouse()
        print "Left mouse clicked"
        self.mouse.emit_click(customInput.BTN_LEFT)

    def clickMouseRight(self):
        if self.mouse == None:
            self.initMouse()
        print "Right mouse clicked"
        self.mouse.emit_click(customInput.BTN_RIGHT)


    def gamepadPressOn(self, joy, key):
        if self.gamepads == None:
            self.initGamepad()

        if key == '5':
            input = customInput.BTN_X

        if key == '6':
            input = customInput.BTN_Y

        if key == '7':
            input = customInput.BTN_Z

        if key == '2':
            input = customInput.BTN_A

        if key == '3':
            input = customInput.BTN_B

        if key == '4':
            input = customInput.BTN_C

        if key == '1':
            input = customInput.BTN_SELECT

        if key == '0':
            input = customInput.BTN_START

        print "key" + str(key) + "was pressed"
        self.gamepads[joy].emit_click(input)

    def gamepadMove(self, joy, xaxis, yaxis):
        if self.gamepads == None:
            self.initGamepad()

        print "joy moved" + str(xaxis) + "," + str(yaxis)
        self.gamepads[joy].emit(customInput.ABS_X, 5 * xaxis, syn=False)
        self.gamepads[joy].emit(customInput.ABS_Y, 5 * yaxis)
