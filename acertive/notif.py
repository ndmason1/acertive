import smtplib
import sys
import traceback 
import syslog

def logNotify(notif):
	syslog.syslog(notif)	

def mailNotify(receivers, notif):
	sender = 'acertive@example.com'	

	message = "From: acertive-daemon <acertive@acertive.d>\n"
	message += "To: Nigel Mason <nigel.mason@carleton.ca>\n"
	message += "Subject: SMTP e-mail test\n\n"
	message += notif

	try:
		smtpObj = smtplib.SMTP('localhost')		
		smtpObj.starttls()
		smtpObj.sendmail(sender, receivers, message)		
		smtpObj.close()
	except smtplib.SMTPException:
		print traceback.format_exc()

def makeNotification(cert, path):
	return "[timestamp] checking certificate " + path + " (issued for) " + cert.get_issuer().commonName


if __name__=='__main__':

	

	