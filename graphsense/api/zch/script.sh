#!/bin/bash
### BEGIN INIT INFO
# Provides: 		script3.sh
# Required-Start: 	$remote_fs $syslog
# Required-Stop: 	$remote_fs $syslog
# Default-Start: 	2 3 4 5
# Default-Stop: 	0 1 6
# Short-Description: 	Start daemon at boot ime
# Description:		nothing to add..
### END INIT INFO
sleep 60

/opt/graphsense-REST/target/universal/stage/bin/graphsense-rest -Dplay.http.secret.key=abcdefghijk

