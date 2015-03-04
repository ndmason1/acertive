import argparse
from checker import (
	trackCert,
	untrackCert,
	checkTrackedCerts,
)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--track', help='track a certificate')
	parser.add_argument('-u', '--untrack', help='stop tracking a certificate')	

	args = parser.parse_args()
	
	if args.track:
		try:
			trackCert(args.track)
		except UserWarning:
			print 'already tracking: ' + os.path.abspath(args.track)
	elif args.untrack:		
		try:
			untrackCert(args.untrack)
		except UserWarning:
			print 'cert not found: ' + os.path.abspath(args.untrack)
	else:
		checkTrackedCerts()

if __name__ == '__main__':
	main()