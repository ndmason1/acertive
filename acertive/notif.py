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


def logNotify(cert, path):
	"""	
	Send a notification to syslog

	:param cert: X509 object corresponding to certificate
	:param path: absolute path of certificate
	"""
	notif = " checking certificate " + os.path.abspath(path)
	notif += " issued for " + cert.get_issuer().commonName
	print notif	
	syslog.syslog(notif)	

def mailNotify(cert, path):
	"""	
	Send a notification to one or more recipients via SMTP

	:param cert: X509 object corresponding to certificate
	:param path: absolute path of certificate
	"""

	sender = 'acertive@acertive.d'	
	receivers = conf.getNotifRecips()

	timestamp = "[" + str(datetime.datetime.now()) + "]"
	notif = timestamp + " checking certificate " + os.path.abspath(path)
	notif += " issued for " + cert.get_issuer().commonName

	message = "From: acertive-daemon <" + sender + ">\n"
	message += "To: <" + receivers[0] + ">\n" #TODO expand list
	message += "Subject: WARNING: Impending certificate expiration!\n\n"
	message += notif

	try:
		smtpObj = smtplib.SMTP('localhost')
		if conf.useTLSWithMail():
			smtpObj.starttls()
		smtpObj.sendmail(sender, receivers, message)
		smtpObj.close()
	except smtplib.SMTPException:
		print traceback.format_exc()