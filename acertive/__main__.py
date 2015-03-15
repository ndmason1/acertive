import argparse
from checker import (
	track_cert,
	untrack_cert,
	check_tracked_certs,
	clear_certs
)
import acertived
import os

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--startd', help='start daemon', action='store_true')
	parser.add_argument('-k', '--stopd', help='stop daemon', action='store_true')
	parser.add_argument('-t', '--track', help='track a certificate')
	parser.add_argument('-u', '--untrack', help='stop tracking a certificate')	
	parser.add_argument('-c', '--clear', help='stop tracking all certificates', action='store_true')	

	args = parser.parse_args()
	
	if args.track:
		try:
			track_cert(args.track)
		except UserWarning:
			print 'already tracking: ' + os.path.abspath(args.track)
	elif args.untrack:		
		try:
			untrack_cert(args.untrack)
		except UserWarning:
			print 'cert not found in tracked certs: ' + os.path.abspath(args.untrack)
	elif args.clear:		
		clear_certs()
	elif args.startd:		
		acertived.run()
	elif args.stopd:		
		acertived.stop()
	else:
		check_tracked_certs()

if __name__ == '__main__':
	main()