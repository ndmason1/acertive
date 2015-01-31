from sys import argv
from  cert import loadCert
from date_util import parseUTCDate, expiresInDays
import notif


def checkTrackedCerts():
	pass

def checkCert(path):
	cert = loadCert(path)
	if expiresInDays(parseUTCDate(cert.get_notAfter()),400):
		notif.notify(cert,path)
	

if __name__=='__main__':
	if (len(argv) > 1):		
		print "processing cert..."
		checkCert(argv[1])
	else:
		print "Please specify a file!"
