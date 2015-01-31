from ConfigParser import SafeConfigParser

def useTLSWithMail():
	return conf.getboolean('MAIL', 'useTLS')

def notifRecips():
	return [conf.get('MAIL', 'notifyAddrs')]

def notifMethod():
	return conf.get('MAIN', 'notifyMethod')

conf = SafeConfigParser()
conf.read('../config.cfg')