import daemon
import lockfile
import os
import signal
import sys
import syslog
import time
import checker

pid_file = '/var/run/acertive/acertived.pid'

def write_PID_file():
	"""	
	Create a PID file to indicate the daemon is running
	"""
	pid = str(os.getpid())
	
	if os.path.isfile(pid_file):		
		sys.exit()
	else:
		file(pid_file, 'w').write(pid+'\n')

def clean_up():
	"""	
	Remove the PID file to indicate the daemon is not running
	"""
	syslog.syslog('terminating...')
	os.unlink(pid_file)

def terminate(signum=None, frame=None):
	"""	
	Clean things up after leaving DaemonContext

	Conforms with the signal handler interface specified at 
	https://docs.python.org/2/library/signal.html

	:param signum: signal number to catch
	:param frame: current stack frame	
	"""
	clean_up()
	sys.exit()

def run():
	"""	
	Start the daemon process, which wakes once per day to check all the tracked 
	certificates
	"""	
	syslog.syslog('starting daemon...')
	context = daemon.DaemonContext(
		pidfile=lockfile.FileLock(pid_file)
	)
	context.signal_map = {
		signal.SIGTERM: terminate
	}
	
	with context:
		syslog.syslog('running as daemon, PID = '+str(os.getpid()))		
		write_PID_file()
		while(True):
			start = time.clock()			
			checker.check_tracked_certs()
			end = time.clock()
			time.sleep((24*60*60) - int(end-start))

def stop():
	"""	
	Stop the daemon process
	"""	
	pid = open(pid_file, 'r').read()
	os.kill(int(pid), signal.SIGTERM)