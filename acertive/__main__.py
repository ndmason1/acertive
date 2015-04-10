import argparse
from checker import (
	track_cert,
	untrack_cert,
	check_tracked_certs,
	clear_certs, 
	list_certs
)
import acertived
import os
import sys

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--startd', help='start daemon', action='store_true')
	parser.add_argument('-k', '--stopd', help='stop daemon', action='store_true')
	parser.add_argument('-t', '--track', \
		help='track a certificate and optionally specify daily/weekly notification thresholds', nargs='+')
	parser.add_argument('-u', '--untrack', help='stop tracking a certificate')	
	parser.add_argument('-c', '--clear', help='stop tracking all certificates', action='store_true')	
	parser.add_argument('-m', '--manualcheck', help='manually check certificates and notify', action='store_true')
	parser.add_argument('-l', '--list', help='list paths of tracked certs', action='store_true')


	args = parser.parse_args()
	
	if args.track:
		try:
			if len(args.track) == 1:
				track_cert(args.track[0])
			elif len(args.track) == 2:
				print "error: must specify thresholds for both daily and weekly!"
				sys.exit(1)
			else:
				d = args.track[1]
				w = args.track[2]
				if w <= d:
					print "error: weekly threshold must be large than daily!"
					sys.exit(1)
				else:
					track_cert(args.track[0], d, w)
		except UserWarning:
			print 'already tracking: ' + os.path.abspath(args.track[0])
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
	elif args.manualcheck:		
		check_tracked_certs(update=False) # do not update lastChecked
	elif args.list:		
		list_certs()
	else:
		parser.print_help()
		sys.exit(1)
		

if __name__ == '__main__':
	main()