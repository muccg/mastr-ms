#
# Regular cron jobs for the mastr-ms package
#
0 4	* * *	root	[ -x /usr/bin/mastr-ms_maintenance ] && /usr/bin/mastr-ms_maintenance
