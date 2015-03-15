import os
from ConfigParser import SafeConfigParser

def notifMethod():
	"""	
	Retrieve notification method to use	
	Supported options: "log" (syslog entries), "mail" (email messages)
	"""
	return conf.get('MAIN', 'notifyMethod')

def storedCertsPath():
	"""	
	Retrieve path of file containing tracked certificates and notification 
	settings
	"""
	return conf.get('MAIN', 'storedCertsFile')

def weekly():
	"""	
	Retrieve config setting for weekly notification threshold value
	"""
	return int(conf.get('MAIN', 'weeklyThreshold'))

def daily():
	"""	
	Retrieve config setting for daily notification threshold value
	"""
	return int(conf.get('MAIN', 'dailyThreshold'))

def SMTPServer():
	"""	
	Retrieve config setting for SMTP server to use for mail notifications
	"""
	return conf.get('MAIL', 'SMTPServerName')

def notifRecips():
	"""	
	Retrieve list of email addresses to send notifications to
	"""
	return conf.get('MAIL', 'notifyAddrs').split(',')

def useTLSWithMail():
	"""	
	Retrieve config setting for attempting to use TLS with SMTP notifications
	"""
	return conf.getboolean('MAIL', 'useTLS')


conf = SafeConfigParser()
app_dir = os.path.dirname(os.path.realpath(__file__))[0:-8]
conf.read(app_dir + 'config.cfg')