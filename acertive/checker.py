import conf
import os
from sys import argv
from  cert import loadCert
from date_util import *
from notif import notify
from datetime import timedelta
import json
import warnings
import argparse


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
			certInfo = json.loads(line)
			if certInfo['path'] == path:
				raise UserWarning()
				return
		certsFile.write(json.dumps({
			'path': path, 
			'weekly': weeklyThreshold, 
			'daily': dailyThreshold,
			'lastChecked': str(datetime.today())
			}) + "\n")

def untrackCert(path):
	"""	
	Remove this certificate from the tracked certs file.

	:param path: location of certificate
	"""

	certsFile = open(conf.storedCertsPath(), 'r')
	lines = certsFile.readlines()	
	certsFile.close()

	removed = False
	certsFile = open(conf.storedCertsPath(), 'w')
	path = os.path.abspath(path)
	for line in lines:
		if json.loads(line)["path"] != path:
			certsFile.write(line)
		else:
			removed = True	
	certsFile.close()
	if not removed:
		raise UserWarning()

def checkTrackedCerts():
	"""	
	Check each tracked certificate for expiration.
	"""
	certsFile = open(conf.storedCertsPath(), 'r')
	lines = certsFile.readlines()	
	certsFile.close()
	for line in lines:		
		certInfo = json.loads(line)

		path = certInfo['path']
		cert = loadCert(path)

		expDate = parseUTCDate(cert.get_notAfter())
		checkedDate = parseUTCDate(certInfo['lastChecked'])		
		today = datetime.today()
		diff = today - checkedDate
		
		if expDate >= today or \
		   today >= expDate - timedelta(days=certInfo['daily']) or \
		   (today >= expDate - timedelta(days=certInfo['weekly']) and \
		   today - checkedDate >= 7):

			print "checking cert at " + certInfo["path"]
			checkCert(certInfo['path'])

def checkCert(path):
	"""	
	Check a certificate for expiration. If the cert is within a notification
	threshold, send a notification.

	:param path: location of certificate
	"""
	cert = loadCert(path)
	days = 400 # TODO extract from certs file
	expireDate = parseUTCDate(cert.get_notAfter())
	if expiresInDays(expireDate,days): 		
		notify(cert,path,daysUntilExpiration(expireDate))
	

if __name__=='__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--track', help='track a certificate')
	parser.add_argument('-u', '--untrack', help='stop tracking a certificate')	

	args = parser.parse_args()
	
	if args.track:
		try:
			trackCert(args.track)
		except UserWarning:
			print 'already tracking: ' + os.path.abspath(args.track)
	elif args.untrack:		
		try:
			untrackCert(args.untrack)
		except UserWarning:
			print 'cert not found: ' + os.path.abspath(args.untrack)
	else:
		checkTrackedCerts()

	# if (len(argv) > 1):		
	# 	try:
			
	# 		trackCert(argv[1])
	# 		#checkTrackedCerts()
	# 		# untrackCert(argv[1])
	# 		#checkCert(argv[1])
			
	# 	except UserWarning:
	# 		print 'already tracking: ' + os.path.abspath(argv[1])
		
	# else:
	# 	checkTrackedCerts()
