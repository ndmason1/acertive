import conf
import os
from sys import argv
from  cert import loadCert
from date_util import parseUTCDate, expiresInDays
from notif import notify
import json
import warnings



def trackCert(path, weeklyThreshold=30, dailyThreshold=7):
	"""	
	Add this certificate to the tracked certs file.

	:param path: location of certificate
	:param weeklyThreshold: number of days from expiration to notify weekly
	:param dailyThreshold: number of days from expiration to notify daily
	"""

	with open(conf.storedCertsPath(), 'a+') as certsFile:		
		path = os.path.abspath(path)
		for line in certsFile:
			if line[0:len(path)] == path:				
				raise UserWarning()
		certsFile.write(json.dumps({'path':path, 'weekly': weeklyThreshold, 
									'daily': dailyThreshold}) + "\n")

def untrackCert(path):
	"""	
	Remove this certificate from the tracked certs file.

	:param path: location of certificate
	"""

	certsFile = open(conf.storedCertsPath(), 'r')
	lines = certsFile.readlines()	
	certsFile.close()

	certsFile = open(conf.storedCertsPath(), 'w')
	path = os.path.abspath(path)
	for line in lines:
		if json.loads(line)["path"] != path:				
			certsFile.write(line)
	certsFile.close()

def checkTrackedCerts():
	"""	
	Check each tracked certificate for expiration.
	"""
	certsFile = open(conf.storedCertsPath(), 'r')
	lines = certsFile.readlines()	
	certsFile.close()
	for line in lines:		
		certInfo = json.loads(line)
		print "checking cert at " + certInfo["path"]
		checkCert(certInfo["path"])


def checkCert(path):
	"""	
	Check a certificate for expiration. If the cert is within a notification
	threshold, send a notification.

	:param path: location of certificate
	"""
	cert = loadCert(path)
	days = 400 # TODO separate based on comments below
	# here, days is an expiration threshold
	if expiresInDays(parseUTCDate(cert.get_notAfter()),days): 
		# here, days is the exact number of days until expiration for this cert
		notify(cert,path,days)
	

if __name__=='__main__':
	
	if (len(argv) > 1):		
		try:
			
			trackCert(argv[1])
			#untrackCert(argv[1])
			#checkCert(argv[1])
			
		except UserWarning:
			print 'already tracking: ' + argv[1]
		
	else:
		checkTrackedCerts()
