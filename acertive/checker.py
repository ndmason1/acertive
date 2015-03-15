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

	:param path: location of certificate
	"""
	with open(conf.stored_certs_path(), 'a+') as certs_file:
		path = os.path.abspath(path)
		if os.path.isfile(path):
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

def check_tracked_certs():
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

		exp_date = parse_UTC_date(cert.get_notAfter())
		checked_date = parse_UTC_date(cert_info['lastChecked'])		
		today = datetime.today()
		diff = today - checked_date
		
		if exp_date >= today or \
		   today >= exp_date - timedelta(days=cert_info['daily']) or \
		   (today >= exp_date - timedelta(days=cert_info['weekly']) and \
		   today - checked_date >= 7):
			
			check_cert(cert_info['path'])

def check_cert(path):
	"""	
	Check a certificate for expiration. If the cert is within a notification
	threshold, send a notification.

	:param path: location of certificate
	"""
	cert = load_cert(path)
	exp_date = parse_UTC_date(cert.get_notAfter())	
	notify(cert,path,days_until_expiration(exp_date))