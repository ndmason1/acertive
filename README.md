# acertive

acertive is a simple tool for keeping track of SSL certificate expiration on Linux platforms.

It includes a daemon that wakes up once per day to check any number of certificates and sends notifications if those certificates are found to be expiring soon (where "soon" can be defined on an individual basis for each certificate, or set to some global value in the configuration). Notifications are sent to the syslog by default, but may also by sent via email (requires a very small amount of configuration).

Daily notifications are sent if the number of days until expiration for a certificate is within a specified amount - the "daily threshold." Similarly, weekly notifications are sent if expiration falls within  the weekly threshold.

Currently, the following certificate filetypes are supported: .cer (DER-encoded), .der, .pem, .crt

## Installation

This package requires an OpenSSL installation for reading certificate files.
Also required is the [setuptools installation framework](https://pypi.python.org/pypi/setuptools).
(This is included with pip, so if you already have that, you're good to go)

1. Download the package (or clone using git)
2. run `sudo python setup.py install` in top level directory of package
3. Edit configuration file (/etc/acertive/config.cfg) to set notification method (set to syslog by default), email adresses to receive notifications, and other settings (see 'Configuraton' section for further details)


## Operation

```
# track certificate stored in <filename>, using threshold values for daily and weekly
# notification if specified (uses default thresholds from configurations otherwise)
# e.g. acertive -t /path/to/cert 10 50  <-- daily threshold of 10, weekly threshold of 50
$ acertive -t, --track <filename> [<daily> <weekly>]

# untrack certificate stored in <filename>
$ acertive -u, --untrack <filename>

# untrack all certificates
$ acertive -c, --clear				

# list tracked certificates and notification thresholds for each
$ acertive -l, --list	

# start the daemon (checks certs once per day and notifies)
$ acertive -s, --startd				

# stop the daemon
$ acertive -k, --stopd				

# manually checks all currently tracked certs and notifies
$ acertive -m, --manualcheck

# show available commands
$ acertive -h, --help
```

Note that a directory may also be passed to the -t option, in which case all certificate files (of a currently supported format) with that directory tree are tracked.

## Configuration

...coming soon...