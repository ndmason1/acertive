
from OpenSSL import crypto
from sys import argv
import getpass

def loadPem(fname):
	pem = open(fname,'rb').read()
	cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem)
	print "opened PEM cert, notAfter is: ", cert.get_notAfter()

def loadDer(fname):
	der = open(fname,'rb').read()
	cert = crypto.load_certificate(crypto.FILETYPE_ASN1, der)
	print "opened DER cert, notAfter is: ", cert.get_notAfter()

def loadPfx(fname):	
	pfx = open(fname,'rb').read()
	pw = getpass.getpass("Export password: ")	
	try:
		cert = crypto.load_pkcs12(pfx,pw).get_certificate()
		print "opened PKCS12 cert, notAfter is: ", cert.get_notAfter()
	except crypto.Error:
		print "bad password! aborting" # TODO allow multiple tries
	

if __name__=='__main__':
	if (len(argv) > 1):
		print "processing cert..."
		if (argv[1][-3:] in 'p12', 'pfx'):
			loadPfx(argv[1])
		elif (argv[1][-3:] in 'pem', 'crt'):
			loadPem(argv[1])
		elif (argv[1][-3:] in 'der', 'cer'):
			loadDer(argv[1])
	else:
		print "Please specify a file!"
