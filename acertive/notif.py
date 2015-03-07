import conf
import datetime
import os
import smtplib
import sys
import traceback 
import syslog


def notify(cert, path, days):	
	"""	
	Send a notification for a soon-to-expire certificate based on the currently 
	configured notification method

	:param cert: X509 object corresponding to certificate
	:param path: absolute path of certificate
	:param days: duration in days until expiration
	"""
	if conf.notifMethod() == 'log':
		logNotify(cert, path, days)
	elif conf.notifMethod() == 'mail':
		mailNotify(cert, path, days)


def logNotify(cert, path, days):
	"""	
	Send a notification to syslog

	:param cert: X509 object corresponding to certificate
	:param path: absolute path of certificate
	:param days: duration in days until expiration
	"""

	m1 = 'certificate from file: ' + os.path.abspath(path)
	m1 += ' (' + cert.get_subject().commonName + ')'
	if days > 0:
		m1 += ' EXPIRES in ' + str(days) + ' days!'
		m2 = 'Please consider RENEWING this certificate soon!'
	else:
		m1 += ' IS EXPIRED!'
		m2 = 'Please RENEW this certificate if it is still in use!'
	
	syslog.syslog(m1)
	syslog.syslog(m2)


def mailNotify(cert, path, days):
	"""	
	Send a notification to one or more recipients via SMTP

	:param cert: X509 object corresponding to certificate
	:param path: absolute path of certificate
	:param days: duration in days until expiration
	"""

	sender = 'acertive@acertive.d'	
	receivers = conf.notifRecips()
	rStr = ''
	for addr in receivers:
		rStr += '<' + addr + '>,'
	rStr = rStr[:-1]
	
	message = 'From: acertive-daemon <' + sender + '>\n'
	message += 'To: ' + rStr + '\n'
	message += 'Subject: WARNING: Impending certificate expiration!\n\n'
	message += '[' + str(datetime.datetime.now()) + ']\n'
	message += 'Certificate from file: ' + os.path.abspath(path) + '\n'
	message += 'Issued for: ' + cert.get_subject().commonName + '\n'
	message += 'Issued by: ' + cert.get_issuer().commonName + '\n\n'
	if days > 0:
		message += 'This certificate is set to EXPIRE in '+str(days)+' days!\n'
		message += 'Please consider renewing this certificate soon.\n'
	else:
		message += 'This certificate has EXPIRED!\n'
		message += 'Please renew the certificate if it is still in use!\n'

	try:
		smtpObj = smtplib.SMTP('localhost') 
		if conf.useTLSWithMail():
			smtpObj.starttls()
		smtpObj.sendmail(sender, receivers, message)
		smtpObj.close()
	except smtplib.SMTPException:
		print traceback.format_exc()