# acertive

An SSL certificate monitoring utility for Linux.

## Installation:

	This package requires an OpenSSL installation for reading certificate files.
	Also required is the [setuptools installation framework](https://pypi.python.org/pypi/setuptools).

	1. Download the package (or clone using git)
	2. run `sudo setup.py install` in top level directory of package
	3. Edit configuration file (config.cfg) to set notification method, 

	(coming soon: PyPI listing)


## Operation:

```
$ acertive					# checks all currently tracked certs and notifies
$ acertive -t <filename>	# track certificate stored in <filename>
$ acertive -u <filename>	# untrack certificate stored in <filename>
$ acertive -s 				# start the daemon (checks certs once per day and notifies)
$ acertive -k 				# stop the daemon
```

(more to come)