import pipCec, time, os

__author__ = 'teixeiras'
from pipInput import pipInput

pipInput = pipInput.pipInput()
pip = pipCec.pipCec(pipInput)
pip.startModule()
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print "Received an kill signal"
    os._exit(1)