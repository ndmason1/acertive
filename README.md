# acertive

An SSL certificate monitoring utility for Linux.

## Installation:

This package requires an OpenSSL installation for reading certificate files.
Also required is the [setuptools installation framework](https://pypi.python.org/pypi/setuptools).
(This is included with pip, so if you already have that, you're good to go)

1. Download the package (or clone using git)
2. run `sudo python setup.py install` in top level directory of package
3. Edit configuration file (/etc/acertive/config.cfg) to set notification method (set to syslog by default), email adresses to receive notifications, and other settings (see below for further details)


## Operation:

```
$ acertive					# checks all currently tracked certs and notifies
$ acertive -t <filename> 	# track certificate stored in <filename>
$ acertive -u <filename>	# untrack certificate stored in <filename>
$ acertive -c				# untrack all certificates
$ acertive -l				# list tracked certificates and notification threshold
$ acertive -s 				# start the daemon (checks certs once per day and notifies)
$ acertive -k 				# stop the daemon
```

Note that a directory may also be passed to the -t option, in which case all certificate files (of a currently supported format) with that directory tree are tracked.