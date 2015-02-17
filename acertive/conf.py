from ConfigParser import SafeConfigParser

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
conf.read('../config.cfg')