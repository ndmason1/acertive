import daemon
import lockfile
import os
import signal
import sys
import syslog
import time
import checker

def createPIDFile():
	"""	
	Create a PID file to indicate the daemon is running
	"""
	pid = str(os.getpid())
	
	if os.path.isfile(pidFile):
		syslog.syslog('PID file exists, exiting')
		sys.exit()
	# else:
	# 	file(pidFile, 'w').write(pid+'\n')

def deletePIDFile():
	"""	
	Remove the PID file to indicate the daemon is not running
	"""
	os.unlink(pidFile)

def setUp():
	"""	
	Set things up before entering DaemonContext
	"""
	createPIDFile()

def tearDown(signum, frame):
	"""	
	Clean things up after leaving DaemonContext

	Conforms with the signal handler interface specified at 
	https://docs.python.org/2/library/signal.html

	TODO: fix this

	:param signum: signal number to catch
	:param frame: current stack frame	
	"""
	deletePIDFile()

def run():
	"""	
	Start the daemon process, which wakes once per day to check all the tracked 
	certificates

	"""
	setUp()

	print "running as daemon, PID = " + str(os.getpid())
	checker.checkTrackedCerts()
	context = daemon.DaemonContext(
		pidfile=lockfile.FileLock(pidFile)
		)
	# context.signal_map = {
	# 	signal.SIGTERM: tearDown,
	# 	signal.SIGHUP: 'terminate'
	# }
	with context:
		while(True):
			syslog.syslog('checking certs')
			checker.checkTrackedCerts()
			time.sleep(24*60*60)

if __name__=='__main__':
	
	global pidFile
	pidFile = '/var/run/acertived.pid'

	run()