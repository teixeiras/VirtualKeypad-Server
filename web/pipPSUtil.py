import psutil, json, sys, traceback
class pipPSUtil(object):
    def __init__(self):
        psutil.cpu_percent(interval=1.0, percpu=True)

    def kill_process(self, processId):
        print "Kill process"+ processId

        p = psutil.Process(processId)
        p.terminate()


    def suspend_process(self, processId):
        p = psutil.Process(processId)
        p.suspend()

    def resume_process(self, processId):
        p = psutil.Process(processId)
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
                process["memory"] = p.memory_percent()
                processes.append(process)
            except:
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60

        output["processes"] = processes
        return json.dumps(output)