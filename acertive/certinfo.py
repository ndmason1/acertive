
from pyasn1_modules import pem, rfc2459
from pyasn1.codec.der import decoder

substrate = pem.readPemFromFile(open('../dummy.crt'))
cert = decoder.decode(substrate, asn1Spec=rfc2459.Certificate())[0]
print(cert.prettyPrint())
