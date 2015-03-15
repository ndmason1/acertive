from nose.tools import *
from acertive.cert import load_pem, load_pem, load_p12

def setup():
	print "SETUP"

def teardown():
	print "SETUP"

def test_load_pem():
	cert = load_pem('test/certs/dummy.crt')
	assert_equal('20150115070726Z',cert.get_notAfter())

def test_load_der():
	cert = load_der('test/certs/dummyder.der')
	assert_equal('20150115070726Z',cert.get_notAfter())

def test_load_p12(): # TODO: fix p/w issue
	pass
	# cert = load_p12('test/certs/example2.com.pfx')
	# assert_equal('20150219203313Z',cert.get_notAfter())