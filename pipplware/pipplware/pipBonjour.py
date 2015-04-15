import select

from pipplware import pybonjour


def register_callback(sdRef, flags, errorCode, name, regtype, domain):
	    if errorCode == pybonjour.kDNSServiceErr_NoError:
	        print 'Registered service:'
	        print '  name    =', name
	        print '  regtype =', regtype
	        print '  domain  =', domain

class pipBonjour(object):
	def __init__(self,name,regtype, port):
		self.sdRef = pybonjour.DNSServiceRegister(name = name,
                                     regtype = regtype,
                                     port = port,
                                     callBack = register_callback)

	def start_module(self):
		while True:
			ready = select.select([self.sdRef], [], [])
			if self.sdRef in ready[0]:
				pybonjour.DNSServiceProcessResult(self.sdRef)




	def __del__(self):
		self.sdRef.close()





