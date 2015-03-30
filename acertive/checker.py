import conf
import os
from  cert import load_cert
from date_util import *
from notif import notify
from datetime import timedelta
import json
import warnings


def track_cert(path):
	"""	
	Add this certificate to the tracked certs file.
	If passed a directory, all certificate files in the directory tree will be 
	tracked.

	:param path: location of certificate or directry containing certificates
	"""
	with open(conf.stored_certs_path(), 'a+') as certs_file:
		path = os.path.abspath(path)

		fmts = ['.cer', '.der', '.crt', '.pem']	

		if os.path.isdir(path):
			for root, dirs, files in os.walk(path):
			    for fname in files:
			    	for fmt in fmts:
				        if fname.endswith(fmt):
				        	certs_file.write(json.dumps({
								'path': os.path.join(root, fname), 
								'weekly': conf.weekly(), 
								'daily': conf.daily(),
								'lastChecked': str(datetime.today())
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
				'weekly': conf.weekly(), 
				'daily': conf.daily(),
				'lastChecked': str(datetime.today())
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

	:param path: location of certificate
	"""
	certs_file = open(conf.stored_certs_path(), 'rw+')
	certs_file.truncate()
	certs_file.close()


def check_tracked_certs(update=True):
	"""	
	Check each tracked certificate for expiration.
	"""
	certs_file = open(conf.stored_certs_path(), 'r')
	lines = certs_file.readlines()	
	certs_file.close()
	for line in lines:		
		cert_info = json.loads(line)

		path = cert_info['path']
		cert = load_cert(path)
		checked_certs = set([])

		exp_date = parse_UTC_date(cert.get_notAfter())
		checked_date = parse_UTC_date(cert_info['lastChecked'])		
		today = datetime.today()
		diff = today - checked_date
		
		if exp_date >= today or \
		   today >= exp_date - timedelta(days=cert_info['daily']) or \
		   (today >= exp_date - timedelta(days=cert_info['weekly']) and \
		   today - checked_date >= 7):
			
			checked_certs.add(cert_info['path'])
			check_cert(cert_info['path'])

	# update lastChecked for each cert that was checked	
	certs_file = open(conf.stored_certs_path(), 'w')	
	for line in lines:
		cert_info = json.loads(line)
		if cert_info['path'] in checked_certs:	
			cert_info['lastChecked'] = str(datetime.today())		
		certs_file.write(json.dumps(cert_info)+'\n')
	certs_file.close()

def check_cert(path):
	"""	
	Check a certificate for expiration. If the cert is within a notification
	threshold, send a notification.

	:param path: location of certificate
	"""
	cert = load_cert(path)
	exp_date = parse_UTC_date(cert.get_notAfter())	
	notify(cert,path,days_until_expiration(exp_date))