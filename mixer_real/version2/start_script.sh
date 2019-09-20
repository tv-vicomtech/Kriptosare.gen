#!/bin/bash
service start msqld
mysql -u mixer -p  db  < /home/bitcoin/table.sql
bitcoind -datadir=/home/bitcoin/.bitcoin/ &
python /home/bitcoin/listener.py
