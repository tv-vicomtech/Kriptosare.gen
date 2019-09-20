#!/bin/bash

sleep 10
addr=$(bitcoin-cli getaccountaddress "")
dt=$(date '+%Y-%m-%d %H:%M:%S')
mysql -u vicomtech -pvicomtech  db -e "insert into accounts (input_address, required_confirmations, secret_mixing_key,created_datetime ) values ('$addr', 0, '','$dt');"
python mixer/listener.py &
python mixer/service.py &

