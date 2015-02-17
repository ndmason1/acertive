import dateutil.parser
from datetime import datetime

def parseUTCDate(utcStr):
	"""	
	Extract a datetime object from a UTC timestamp

	:param utcStr: UTC timestamp
	"""
	return dateutil.parser.parse(utcStr)
	
def expiresInDays(dateTime, numDays):
	"""	
	Return true if given datetime occurs within a specified number of days from 
	today

	:param dateTime: datetime object representing an expiry date
	:param numDays: duration in days from now after which the cert corresponding
		to the given datetime is considered expired
	"""
	diff = dateTime - datetime.now(dateutil.tz.tzutc())
	return diff.total_seconds() <= numDays*24*60*60
	

if __name__=='__main__':
	
	d1 = parseUTCDate('20150407070726Z')
	d2 = parseUTCDate('20150120070726Z')	
	print expiresInDays(d1,1000)
	