#!/bin/bash
### BEGIN INIT INFO
# Provides: 		script2.sh
# Required-Start: 	$remote_fs $syslog
# Required-Stop: 	$remote_fs $syslog
# Default-Start: 	2 3 4 5
# Default-Stop: 	0 1 6
# Short-Description: 	Start daemon at boot ime
# Description:		nothing to add..
### END INIT INFO

sleep 40

cd /opt/graphsense-datafeed
/usr/bin/cqlsh -f schema_raw.cql
RES=$(curl --user uab:uabpassword --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [0] }' -H 'content-type: text/plain;' http://bitcoin_probe:18332 | jq -r '.result')
sed -i 's/BLOCK_0 =.*/BLOCK_0 = "'$RES'"/' /opt/graphsense-datafeed/fetch_blocks.py
sed -i 's/BLOCK_0 =.*/BLOCK_0 = "'$RES'"/' /opt/graphsense-datafeed/continuous_ingest.py
sed -i 's/BLOCK_0 =.*/BLOCK_0 = "'$RES'"/' /opt/graphsense-datafeed/continuous_ingest_mod.py

python3 /opt/graphsense-datafeed/continuous_ingest_mod.py -h bitcoin_probe -p 18332 -c localhost -s 300 > tx.txt
#/etc/init.d/script3.sh


