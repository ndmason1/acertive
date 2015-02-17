import dateutil.parser
from datetime import datetime

def parseUTCDate(utcStr):
	"""	
	Extract a datetime object from a UTC timestamp

	:param utcStr: UTC timestamp
	"""
	return dateutil.parser.parse(utcStr,ignoretz=True)

def daysUntilExpiration(dateTime):
	"""	
	Returns number of days until the given dateTime

	:param dateTime: datetime object representing an expiry date
	"""	
	diff = dateTime - datetime.today()
	return diff.days

	
def expiresInDays(dateTime, numDays):
	"""	
	Return true if given datetime occurs within a specified number of days from 
	today

	:param dateTime: datetime object representing an expiry date
	:param numDays: duration in days from now after which the cert corresponding
		to the given datetime is considered expired
	"""	
	diff = dateTime - datetime.today()
	return diff.days <= numDays
	

if __name__=='__main__':
	d1 = parseUTCDate('20150218230726Z')	
	print 'days until exp: ' + str(daysUntilExpiration(d1))
	