import json
import sys
import traceback
from sys import platform as _platform

from pipplware.pipLog import pipLog

import psutil
#from pipplware.web.vcgencmd import vcgencmd


class pipPSUtil(object):
    def __init__(self):
        psutil.cpu_percent(interval=1.0, percpu=True)

    def kill_process(self, processId):
        pipLog.sharedInstance.debug( "Kill process"+ processId)

        p = psutil.Process(int(float(processId)))
        p.terminate()


    def suspend_process(self, processId):
        pipLog.sharedInstance.debug( "Suspense process"+ processId)
        p = psutil.Process(int(float(processId)))
        p.suspend()

    def resume_process(self, processId):
        pipLog.sharedInstance.debug( "Resume process"+ processId)
        p = psutil.Process(int(float(processId)))
        p.resume()


    def output(self):
        output = {}
        #processor
        output["number_of_processors"] = psutil.cpu_count()
        output["cpu_percent"] = psutil.cpu_percent(interval=None, percpu=True)
        output["memory"] = psutil.virtual_memory()
        output["swap"] = psutil.swap_memory()
        output["partitions"] = psutil.disk_partitions()

        output["mountpoints"] = {};
        for value in output["partitions"]:
            output["mountpoints"][value.mountpoint] = psutil.disk_usage(value.mountpoint)

        processes = []

        """ processes = []
        for p in psutil.process_iter():
             processes.append(p)
        output["process_list"] = processes
        """


        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                process = {}
                process["pid"] = p.pid
                process["name"] = p.name()
                process["cmdline"] = p.cmdline()
                process["cpu"] = p.cpu_percent(interval=None)
                process["memory"] = round(p.memory_percent(),2)
                processes.append(process)
            except:
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60

        output["processes"] = processes
        """
        if _platform != "darwin":

           # output['ClockFrequencies']={"sources": vcgencmd.frequency_sources(),
           #                             "value": vcgencmd.measure_clock}

            output['Voltages']={"sources": vcgencmd.voltage_sources(),
                                "value": vcgencmd.measure_volts}

            #output['Temperatures']={"values": vcgencmd.measure_temp()}

            output['Codecs']={"sources": vcgencmd.codec_sources(),
                                "value": vcgencmd.codec_enabled}

            output['MemoryAllocation']={"sources": vcgencmd.memory_sources(),
                                "value": vcgencmd.get_mem}
        """

        return json.dumps(output)