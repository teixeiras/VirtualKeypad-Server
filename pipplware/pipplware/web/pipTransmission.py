import json

from pipplware.web import transmissionrpc


class pipTransmission(object):
    def __init__(self, port=9091, user="pi", password="raspberry"):
        try:
            self.tc = transmissionrpc.Client('localhost', port, user, password)
        except:
            self.tc = None

    def output(self):
        output = {"status":"1"}
        if self.tc == None:
            return output

        output["torrents"] = []
        for torrent in self.tc.get_torrents():
            torrentObj = {"name":torrent.get_name_string(),
                          "status":torrent._status(),
                          "progress":torrent.progress
                }
            output["torrents"].append(torrentObj)



        return json.dumps(output)

    def addFile(self, filePath):
        if self.tc == None:
            return

        self.tc.add_torrent("file://" + filePath)

    def add(self, uri):
        if self.tc == None:
            return

        self.tc.add_torrent(uri)
        return  json.dumps({"status":"1"})