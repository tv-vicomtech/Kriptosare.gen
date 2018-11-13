#!/bin/bash
### BEGIN INIT INFO
# Provides: 		my_script.sh
# Required-Start: 	$remote_fs $syslog
# Required-Stop: 	$remote_fs $syslog
# Default-Start: 	2 3 4 5
# Default-Stop: 	0 1 6
# Short-Description: 	Start daemon at boot ime
# Description:		nothing to add..
### END INIT INFO

python /opt/graphite/bin/carbon-cache.py start
python opt/graphite/bin/carbon-aggregator.py start
/usr/sbin/nginx -c /etc/nginx/nginx.conf
nodejs /opt/statsd/stats.js /opt/statsd/config_udp.js &
python /opt/graphite/webapp/graphite/manage.py runfcgi daemonize=false host=127.0.0.1 port=8080 &
service grafana-server restart
bitcoind -datadir=/root/.bitcoin
exit 0
