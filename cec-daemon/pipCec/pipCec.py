#!/usr/bin/python

import re
import os
import subprocess

from pipplware.pipInput import customInput


class pipCec(object):
    def __init__(self, pipInputObject):
        self.pipInputObject = pipInputObject
        self.exactMatch = re.compile(r'key released: (\w+)', flags=re.IGNORECASE)
        self.DEVNULL = open(os.devnull, 'wb')

    def start_module(self):
        print  "CEC Module started..."
        proc = subprocess.Popen(['/usr/bin/cec-client',''],stdout=subprocess.PIPE,stderr=self.DEVNULL)
        for line in iter(proc.stdout.readline,''):
            for key in self.exactMatch.findall(line.rstrip()):
                print "Key was pressed: "+key
                if key == "up":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_UP)

                elif key == "left":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_LEFT)

                elif key == "right":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_RIGHT)

                elif key == "down":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_DOWN)

                elif key == "enter" or key == "select":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_ENTER)

                elif key == "exit" or key == "return":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_BACKSPACE)

                elif key == "F4":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_RIGHTSHIFT)

                elif key == "F1":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_RIGHTCTRL)

                elif key == "F3":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_PAGEUP)

                elif key == "F2":
                    self.pipInputObject.sendKeyUsingEvent(customInput.KEY_PAGEDOWN)

    def __del__(self):
        self.DEVNULL.close()




#os.system("killall -9 cec-client");


