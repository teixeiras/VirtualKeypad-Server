import psutil, json
class pipPSUtil(object):
    def __init__(self):
        psutil.cpu_percent(interval=1.0, percpu=True)

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
        for pid in psutil.pids():
            p = psutil.Process(pid)
            process = {}
            process["name"] = p.name()
            process["cmdline"] = p.cmdline()
            process["cpu"] = p.cpu_percent(interval=None)
            process["memory"] = p.memory_percent()
            processes.append(process)
        output["processes"] = processes
        return json.dumps(output)