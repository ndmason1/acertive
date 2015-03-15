import dateutil.parser
from datetime import datetime

def parse_UTC_date(utc_str):
	"""	
	Extract a datetime object from a UTC timestamp

	:param utc_str: UTC timestamp
	"""
	return dateutil.parser.parse(utc_str,ignoretz=True)

def days_until_expiration(date_time):
	"""	
	Returns number of days until the given dateTime

	:param date_time: datetime object representing an expiry date
	"""	
	diff = date_time - datetime.today()
	return diff.days

	
def expires_in_days(date_time, num_days):
	"""	
	Return true if given datetime occurs within a specified number of days from 
	today

	:param date_time: datetime object representing an expiry date
	:param num_days: duration in days from now after which the cert corresponding
		to the given datetime is considered expired
	"""	
	diff = date_time - datetime.today()
	return diff.days <= num_days
	

if __name__=='__main__':
	d1 = parse_UTC_date('20150218230726Z')	
	print 'days until exp: ' + str(days_until_expiration(d1))
	