from OpenSSL import crypto
from sys import argv
import getpass
import dateparser
import notif

def loadCert(fname):
	print "loading cert: " + fname
	if (fname[-3:] in ['p12', 'pfx']):
		cert = loadP12(fname)		
	elif (fname[-3:] in ['pem', 'crt']): # these could be .cer as well?
		cert = loadPem(fname)			
	elif (fname[-3:] in ['der', 'cer']):
		cert = loadDer(fname)
	return cert

def loadDer(fname):
	with open(fname,'rb') as der:
		cert = crypto.load_certificate(crypto.FILETYPE_ASN1, der.read())
		print "opened DER cert, notAfter is: ", cert.get_notAfter()
		return cert

def loadPem(fname):
	with open(fname,'rb') as pem:	
		cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem.read())
		print "opened PEM cert, notAfter is: ", dateparser.parseUTCDate(cert.get_notAfter())
		return cert

def loadP12(fname):	
	with open(fname,'rb') as p12:
		pw = getpass.getpass("Export password: ")	
		try:
			cert = crypto.load_pkcs12(p12.read(),pw).get_certificate()
			print "opened PKCS12 cert, notAfter is: ", dateparser.parseUTCDate(cert.get_notAfter())
			return cert
		except crypto.Error:
			print "bad password! aborting" # TODO allow multiple tries
	

if __name__=='__main__':
	if (len(argv) > 1):		
		print "processing cert..."
		loadCert(argv[1])
	else:
		print "Please specify a file!"
