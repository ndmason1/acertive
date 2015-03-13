import daemon
import lockfile
import os
import signal
import sys
import syslog
import time
import checker

pidFile = '/var/run/acertived.pid'

def writePIDFile():
	"""	
	Create a PID file to indicate the daemon is running
	"""
	pid = str(os.getpid())
	
	if os.path.isfile(pidFile):		
		sys.exit()
	else:
		file(pidFile, 'w').write(pid+'\n')

def cleanUp():
	"""	
	Remove the PID file to indicate the daemon is not running
	"""
	syslog.syslog('cleaning up for termination')
	os.unlink(pidFile)

def terminate(signum=None, frame=None):
	"""	
	Clean things up after leaving DaemonContext

	Conforms with the signal handler interface specified at 
	https://docs.python.org/2/library/signal.html

	:param signum: signal number to catch
	:param frame: current stack frame	
	"""
	cleanUp()
	sys.exit()

def run():
	"""	
	Start the daemon process, which wakes once per day to check all the tracked 
	certificates
	"""	

	context = daemon.DaemonContext(
		pidfile=lockfile.FileLock(pidFile)
	)
	context.signal_map = {
		signal.SIGTERM: terminate
	}

	with context:
		syslog.syslog('running as daemon, PID = '+str(os.getpid()))		
		writePIDFile()
		while(True):
			start = time.clock()			
			checker.checkTrackedCerts()
			end = time.clock()
			time.sleep((24*60*60) - int(end-start))

def stop():
	"""	
	Stop the daemon process
	"""
	pidFile = '/var/run/acertived.pid'
	pid = open(pidFile, 'r').read()
	os.kill(int(pid), signal.SIGTERM)