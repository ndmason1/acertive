import os
from ConfigParser import SafeConfigParser

#TODO add SMTP server as config item

def useTLSWithMail():
	"""	
	Retrieve config setting for attempting to use TLS with SMTP notifications
	"""
	return conf.getboolean('MAIL', 'useTLS')

def notifRecips():
	"""	
	Retrieve list of email addresses to send notifications to
	"""
	return [conf.get('MAIL', 'notifyAddrs')]

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

conf = SafeConfigParser()
app_dir = os.path.dirname(os.path.realpath(__file__))[0:-8]
conf.read(app_dir + 'config.cfg')