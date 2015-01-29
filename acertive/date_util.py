import dateutil.parser
from datetime import datetime

def parseUTCDate(utcStr):
	return dateutil.parser.parse(utcStr)
	
def expiresInDays(dateTime, numDays):
	diff = dateTime - datetime.now(dateutil.tz.tzutc())
	return diff.total_seconds() <= numDays*24*60*60
	

if __name__=='__main__':
	
	d1 = parseUTCDate('20150407070726Z')
	d2 = parseUTCDate('20150120070726Z')	
	print expiresInDays(d1,1000)
	