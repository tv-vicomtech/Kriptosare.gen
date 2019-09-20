#!/bin/bash
### BEGIN INIT INFO
# Provides: 		script.sh
# Required-Start: 	$remote_fs $syslog
# Required-Stop: 	$remote_fs $syslog
# Default-Start: 	2 3 4 5
# Default-Stop: 	0 1 6
# Short-Description: 	Start daemon at boot time
# Description:		nothing to add..
### END INIT INFO

IP=$(getent hosts btc_api | awk '{ print $1 }')

sed -ie 's/localhost/'$IP'/g' /srv/graphsense-dashboard/dashboard.py
sed -i '1s/^/daemon off;\n/' /etc/nginx/nginx.conf

/etc/init.d/uwsgi start
service nginx start
