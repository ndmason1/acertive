import conf
import os
from sys import argv
from  cert import loadCert
from date_util import parseUTCDate, expiresInDays
from notif import notify
import json
import warnings

def trackCert(path):
	with open(conf.storedCertsPath(), 'a+') as certsFile:		
		path = os.path.abspath(path)
		for line in certsFile:
			if line[0:-1] == path:				
				raise RuntimeWarning()
		certsFile.write(path+'\n')

def untrackCert(path):
	with open(conf.storedCertsPath(), 'r+') as certsFile:		
		path = os.path.abspath(path)
		for line in certsFile:
			if line[0:-1] == path:				
				return

def checkTrackedCerts():
	pass

def checkCert(path):
	cert = loadCert(path)
	if expiresInDays(parseUTCDate(cert.get_notAfter()),400):
		notify(cert,path)
	

if __name__=='__main__':
	if (len(argv) > 1):		
		try:
			trackCert(argv[1])
			#checkCert(argv[1])
		except RuntimeWarning:
			print 'already tracking: ' + argv[1]
		
	else:
		print 'Please specify a file!'
