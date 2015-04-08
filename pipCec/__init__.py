import pipCec, time, os

__author__ = 'teixeiras'
from pipInput import pipInput
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



