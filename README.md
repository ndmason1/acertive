# acertive

An SSL certificate monitoring utility for Linux.


Operation:

```
$ acertive					# checks all currently tracked certs and notfies
$ acertive -t <filename>	# track certificate stored in <filename>
$ acertive -u <filename>	# untrack certificate stored in <filename>
$ acertive -s 				# start the daemon (checks certs once per day and notifies)
$ acertive -k 				# checks all currently tracked certs
```