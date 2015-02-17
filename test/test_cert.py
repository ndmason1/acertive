from nose.tools import *
from acertive.cert import loadPem, loadDer, loadP12

def setup():
	print "SETUP"

def teardown():
	print "SETUP"

def test_load_pem():
	cert = loadPem('test/certs/dummy.crt')
	assert_equal('20150115070726Z',cert.get_notAfter())

def test_load_der():
	cert = loadDer('test/certs/dummyder.der')
	assert_equal('20150115070726Z',cert.get_notAfter())

def test_load_p12():
	cert = loadP12('test/certs/example2.com.pfx')
	assert_equal('20150219203313Z',cert.get_notAfter())