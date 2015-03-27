#!/usr/bin/python

import re
import os
import subprocess

import uinput


class pipCec(object):

        def __init__(self, pipInputObject):
            self.pipInputObject = pipInputObject
            self.exactMatch = re.compile(r'key released: (\w+)', flags=re.IGNORECASE)
            self.DEVNULL = open(os.devnull, 'wb')

        def startModule(self):
                proc = subprocess.Popen(['/usr/bin/cec-client',''],stdout=subprocess.PIPE,stderr=self.DEVNULL)
                for line in iter(proc.stdout.readline,''):
                        for key in self.exactMatch.findall(line.rstrip()):
                                print "Key was pressed: "+key

                                if key == "up":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_UP)

                                elif key == "left":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_LEFT)

                                elif key == "right":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_RIGHT)

                                elif key == "down":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_DOWN)

                                elif key == "enter" or key == "select":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_ENTER)

                                elif key == "exit" or key == "return":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_BACKSPACE)

                                elif key == "F4":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_RIGHTSHIFT)

                                elif key == "F1":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_RIGHTCTRL)

                                elif key == "F3":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_PAGEUP)

                                elif key == "F2":
                                        self.pipInputObject.sendKeyUsingEvent(uinput.KEY_PAGEDOWN)

        def __del__(self):
                self.DEVNULL.close()   


       

#os.system("killall -9 cec-client");


