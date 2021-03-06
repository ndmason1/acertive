import os
from ConfigParser import SafeConfigParser

def notif_method():
	"""	
	Retrieve notification method to use	
	Supported options: "log" (syslog entries), "mail" (email messages), "both"
	"""
	return conf.get('MAIN', 'notifyMethod')

def stored_certs_path():
	"""	
	Retrieve path of file containing tracked certificates and notification 
	settings
	"""
	return conf.get('MAIN', 'storedCertsFile')

def weekly():
	"""	
	Retrieve config setting for default weekly notification threshold value
	"""
	return int(conf.get('MAIN', 'weeklyThreshold'))

def daily():
	"""	
	Retrieve config setting for default daily notification threshold value
	"""
	return int(conf.get('MAIN', 'dailyThreshold'))

def SMTP_server():
	"""	
	Retrieve config setting for SMTP server to use for mail notifications
	"""
	return conf.get('MAIL', 'SMTPServerName')

def notif_recips():
	"""	
	Retrieve list of email addresses to send notifications to
	"""
	return conf.get('MAIL', 'notifyAddrs').split(',')

def use_TLS_with_mail():
	"""	
	Retrieve config setting for attempting to use TLS with SMTP notifications
	"""
	return conf.getboolean('MAIL', 'useTLS')

def sender_email():
	"""	
	Retrieve config setting for sender email address
	"""
	return conf.get('MAIL', 'senderAddr')


conf = SafeConfigParser()
app_dir = os.path.dirname(os.path.realpath(__file__))[0:-8]
conf.read('/etc/acertive/config.cfg')