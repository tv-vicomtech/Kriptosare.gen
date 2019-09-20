#!/bin/bash
### BEGIN INIT INFO
# Provides: 		script1.sh
# Required-Start: 	$remote_fs $syslog
# Required-Stop: 	$remote_fs $syslog
# Default-Start: 	2 3 4 5
# Default-Stop: 	0 1 6
# Short-Description: 	Start daemon at boot time
# Description:		nothing to add..
### END INIT INFO
IP=$(ip addr | grep inet | grep eth0 | awk -F" " '{print $2}'| sed -e 's/\/.*$//')
sed -i '/listen_address: /c\listen_address: '$IP /etc/cassandra/cassandra.yaml
sed -i '/start_rpc: /c\start_rpc: true ' /etc/cassandra/cassandra.yaml
sed -i '/rpc_address: localhost/c\rpc_address: 0.0.0.0' /etc/cassandra/cassandra.yaml
sed -i '/# broadcast_rpc_address: /c\broadcast_rpc_address: '$IP /etc/cassandra/cassandra.yaml
sed -i '/- seeds: /c\        - seeds: '$IP /etc/cassandra/cassandra.yaml


bash /etc/init.d/script21.sh &
cassandra -fR 

