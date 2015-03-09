import daemon
import lockfile
import os
import signal
import sys
import syslog
import time
import checker

def createPIDFile():
	global pidFile
	"""	
	Create a PID file to indicate the daemon is running
	"""
	pid = str(os.getpid())
	
	if os.path.isfile(pidFile):
		sys.exit()
	else:
		file(pidFile, 'w').write(pid+'\n')

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
	syslog('cleaning up for termination')
	deletePIDFile()

def run():
	"""	
	Start the daemon process, which wakes once per day to check all the tracked 
	certificates

	"""
	global pidFile
	pidFile = '/var/run/acertived.pid'

	setUp()
	checker.checkTrackedCerts()
	context = daemon.DaemonContext(
		pidfile=lockfile.FileLock(pidFile)
		)
	context.signal_map = {
		signal.SIGTERM: tearDown
	}
	with context:
		syslog.syslog('running as daemon, PID = '+str(os.getpid()))
		while(True):
			start = time.clock()			
			checker.checkTrackedCerts()
			end = time.clock()
			time.sleep((24*60*60) - int(end-start))

if __name__=='__main__':
	run()