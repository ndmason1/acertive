import daemon
import lockfile
import os
import signal
import sys
import syslog
import time

def createPIDFile():
	pid = str(os.getpid())
	
	if os.path.isfile(pidFile):
		syslog.syslog('PID file exists, exiting')
		sys.exit()
	# else:
	# 	file(pidFile, 'w').write(pid+'\n')

def deletePIDFile():
	os.unlink(pidFile)

def setUp():
	createPIDFile()

def tearDown(signum, frame):
	deletePIDFile()

def run():
	setUp()

	print "running as daemon, PID = " + str(os.getpid())
	context = daemon.DaemonContext(
		pidfile=lockfile.FileLock(pidFile)
		)
	context.signal_map = {
		signal.SIGTERM: tearDown,
		signal.SIGHUP: 'terminate'
	}
	with context:
		while(True):
			syslog.syslog("checking certs")
			time.sleep(24*60*60)

if __name__=='__main__':
	
	global pidFile
	pidFile = '/var/run/acertived.pid'

	run()