import conf
import datetime
import os
import smtplib
import sys
import traceback 
import syslog


def notify(cert, path):	
	"""	
	Send a notification for a soon-to-expire certificate based on the currently 
	configured notification method

	:param cert: X509 object corresponding to certificate
	:param path: absolute path of certificate
	"""
	if conf.notifMethod() == 'log':
		logNotify(cert, path)
	elif conf.notifMethod == 'mail':
		mailNotify(cert, path)


def logNotify(cert, path, days):
	"""	
	Send a notification to syslog

	:param cert: X509 object corresponding to certificate
	:param path: absolute path of certificate
	:param days: duration in days until expiration
	"""

	message = 'certificate from file: ' + os.path.abspath(path)
	message += ' (' + cert.get_issuer().commonName + ') EXPIRES in '
	message += str(days) + ' days!'
	print message	
	syslog.syslog(message)	

def mailNotify(cert, path, days):
	"""	
	Send a notification to one or more recipients via SMTP

	:param cert: X509 object corresponding to certificate
	:param path: absolute path of certificate
	:param days: duration in days until expiration
	"""

	sender = 'acertive@acertive.d'	
	receivers = conf.getNotifRecips()
	
	message = 'From: acertive-daemon <' + sender + '>\n'
	message += 'To: <' + receivers[0] + '>\n' #TODO expand list
	message += 'Subject: WARNING: Impending certificate expiration!\n\n'
	message += '[' + str(datetime.datetime.now()) + ']\n'
	message += 'Certificate from file: ' + os.path.abspath(path) + '\n'
	message += 'Issued for :' + cert.get_issuer().commonName + '\n\n'
	message += 'This certificate is set to EXPIRE in ' + str(days) + ' days!\n'
	message += 'Please consider renewing this certificate soon.\n'

	try:
		smtpObj = smtplib.SMTP('localhost') 
		if conf.useTLSWithMail():
			smtpObj.starttls()
		smtpObj.sendmail(sender, receivers, message)
		smtpObj.close()
	except smtplib.SMTPException:
		print traceback.format_exc()