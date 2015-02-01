import conf
import os
from sys import argv
from  cert import loadCert
from date_util import parseUTCDate, expiresInDays
import notif


def trackCert(path):
	with open(conf.storedCertsPath(), 'a+') as certsFile:		
		path = os.path.abspath(path)
		for line in certsFile:
			if line[0:-1] == path:				
				return		
		certsFile.write(path+'\n')

def checkTrackedCerts():
	pass

def checkCert(path):
	cert = loadCert(path)
	if expiresInDays(parseUTCDate(cert.get_notAfter()),400):
		notif.notify(cert,path)
	

if __name__=='__main__':
	if (len(argv) > 1):		
		print "processing cert..."
		trackCert(argv[1])
		#checkCert(argv[1])
	else:
		print "Please specify a file!"
