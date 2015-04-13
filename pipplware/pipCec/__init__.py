import time
import os

from pipplware.pipCec.pipCec import pipCec
from pipplware.pipCec import pipCec
from pipplware.pipInput import pipInput


__author__ = 'teixeiras'
if __name__ == '__main__':
    pipInput = pipInput.pipInput()
    pip = pipCec.pipCec(pipInput)
    pip.start_module()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print "Received an kill signal"
        os._exit(1)



