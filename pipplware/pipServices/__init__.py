__author__ = 'teixeiras'
import re
from os import listdir

exactMatch = re.compile(r'rc(\w+).d', flags=re.IGNORECASE)

for etc in  listdir("/etc/"):
    for rc in exactMatch.findall(etc):
        print "Found rc" + rc
        rcs = [ f for f in listdir("/etc/rc"+rc+".d")]
        print "Services on rc" + rc
        print rcs

