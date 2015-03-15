from OpenSSL import crypto
import getpass

def load_cert(fname):	
	"""	
	Load an X.509 certificate from the specified file

	:param fname: absolute path of cert file
	"""
	if (fname[-3:] in ['p12', 'pfx']):
		cert = load_p12(fname)		
	elif (fname[-3:] in ['pem', 'crt']):
		cert = load_pem(fname)			
	elif (fname[-3:] in ['der', 'cer']):
		cert = load_der(fname)
	else:
		raise NotImplementedError('file format not accepted')
	return cert

def load_der(fname):
	"""	
	Load a DER-formatted X.509 certificate from the specified file

	:param fname: absolute path of cert file
	"""
	with open(fname,'rb') as der:
		cert = crypto.load_certificate(crypto.FILETYPE_ASN1, der.read())
		return cert

def load_pem(fname):
	"""	
	Load a PEM-formatted X.509 certificate from the specified file

	:param fname: absolute path of cert file
	"""
	with open(fname,'rb') as pem:	
		cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem.read())
		return cert

def load_p12(fname):
	"""	
	Load a PKCS12-formatted X.509 certificate from the specified file

	:param fname: absolute path of cert file
	"""	
	with open(fname,'rb') as p12:
		pw = getpass.getpass("Export password: ")	
		try:
			cert = crypto.load_pkcs12(p12.read(),pw).get_certificate()
			return cert
		except crypto.Error:
			print "bad password! aborting" # TODO allow multiple tries