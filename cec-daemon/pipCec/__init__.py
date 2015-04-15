from pipCec import pipCec
from pipplware.pipInput import pipInput

__author__ = 'teixeiras'
import time
import os

pipInput = pipInput.pipInput()

__author__ = 'teixeiras'
def main():
    pip = pipCec(pipInput)
    pip.start_module()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print "Received an kill signal"
        os._exit(1)

if __name__ == '__main__':
    main()
