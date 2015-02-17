from nose.tools import *
from datetime import timedelta
from acertive.date_util import *

def test_parse_UTC():
	d1 = parseUTCDate('20150407070726Z')
	assert_equal('2015-04-07 07:07:26+00:00',str(d1))

def test_exp_in_days():
	d1 = parseUTCDate('20150407070726Z')
	assert_equal(True,expiresInDays(d1,1000))

def test_days_until_exp():	
	num_days = 7;	
	today = datetime.today()
	# add a minute so the processing time doesn't push the difference back too far
	d1 = today + timedelta(days=num_days,minutes=1) 
	assert_equal(num_days,daysUntilExpiration(d1))
