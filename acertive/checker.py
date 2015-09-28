import conf
import os
from  cert import load_cert
from date_util import *
from notif import notify
from datetime import timedelta
import json
import warnings

def track_cert(path, daily=conf.daily(), weekly=conf.weekly()):
	"""	
	Add this certificate to the tracked certs file.
	If passed a directory, all certificate files in the directory tree will be 
	tracked.

	:param path: location of certificate or directry containing certificates
	:param daily: number of days until expiration in which daily notifications activate
	:param weekly: number of weeks until expiration in which weekly notifications activate
	"""
	with open(conf.stored_certs_path(), 'a+') as certs_file:
		path = os.path.abspath(path)

		fmts = ['.cer', '.der', '.crt', '.pem']	

		init_date = datetime.today() - timedelta(days=8)

		if os.path.isdir(path):
			for root, dirs, files in os.walk(path):
			    for fname in files:
			    	for fmt in fmts:
				        if fname.endswith(fmt):
				        	certs_file.write(json.dumps({
								'path': os.path.join(root, fname), 
								'weekly': str(weekly), 
								'daily': str(daily),
								'lastNotified': str(init_date)
								}) + "\n")

		elif os.path.isfile(path):
			if path[-4:] not in fmts:
				print "file format not accepted: must be one of " + str(fmts)

			for line in certs_file:
				cert_info = json.loads(line)
				if cert_info['path'] == path:
					raise UserWarning()
					return
			certs_file.write(json.dumps({
				'path': path, 
				'weekly': str(weekly), 
				'daily': str(daily),
				'lastNotified': str(init_date)
				}) + "\n")
		else:
			print "no such file: " + path

def untrack_cert(path):
	"""	
	Remove this certificate from the tracked certs file.

	:param path: location of certificate
	"""

	certs_file = open(conf.stored_certs_path(), 'r')
	lines = certs_file.readlines()	
	certs_file.close()

	removed = False
	certs_file = open(conf.stored_certs_path(), 'w')
	path = os.path.abspath(path)
	for line in lines:
		if json.loads(line)["path"] != path:
			certs_file.write(line)
		else:
			removed = True	
	certs_file.close()
	if not removed:
		raise UserWarning()

def clear_certs():
	"""	
	Remove all certificates from the tracked certs file.
	"""
	certs_file = open(conf.stored_certs_path(), 'rw+')
	certs_file.truncate()
	certs_file.close()


def check_tracked_certs(update=True):
	"""	
	Check each tracked certificate for expiration.
	Initiate a notification if expiration falls within a threshold.

	:param update: true if the lastNotified field of a cert should be updated, false otherwise
	"""
	certs_file = open(conf.stored_certs_path(), 'r')
	lines = certs_file.readlines()	
	certs_file.close()	
	notified_certs = set([])

	for line in lines:		
		cert_info = json.loads(line)

		path = cert_info['path']
		cert = load_cert(path)		

		exp_date = parse_UTC_date(cert.get_notAfter())
		notified_date = parse_UTC_date(cert_info['lastNotified'])		
		today = datetime.today()
		diff = today - notified_date
		days = days_until_expiration(exp_date)

		if exp_date <= today or days <= int(cert_info['daily']):
			# already expired or within daily threshold
			notified_certs.add(cert_info['path'])
			check_cert(cert_info)
		elif days <= int(cert_info['weekly']) and (diff.days >= 7 or not update):
			# within weekly threshold: notify only if a week has passed since
			# last notification, or if it is being manually checked
			notified_certs.add(cert_info['path'])
			check_cert(cert_info)

	if update:		
		# update lastNotified for each cert that was checked	
		certs_file = open(conf.stored_certs_path(), 'w')	
		for line in lines:
			cert_info = json.loads(line)			
			if cert_info['path'] in notified_certs:					
				cert_info['lastNotified'] = str(datetime.today())		
			certs_file.write(json.dumps(cert_info)+'\n')
		certs_file.close()

def list_certs():
	"""	
	Prints the path of each tracked cert.
	"""
	certs_file = open(conf.stored_certs_path(), 'r')
	lines = certs_file.readlines()	
	certs_file.close()
	for line in lines:		
		cert_info = json.loads(line)
		print cert_info['path'] + ' daily:' + cert_info['daily'] + ' weekly:' + cert_info['weekly']

def check_cert(cert_info):
	"""	
	Check a certificate for expiration. If the cert is within a notification
	threshold, send a notification.
	
	:param cert_info: dict containing tracked cert information
	"""
	cert = load_cert(cert_info['path'])
	exp_date = parse_UTC_date(cert.get_notAfter())
	days = days_until_expiration(exp_date)
	notify(cert, cert_info['path'], days)