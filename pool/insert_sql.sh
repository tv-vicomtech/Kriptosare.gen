#!/bin/bash
mysqlimport --fields-terminated-by=, --columns='tx_rec,amount_rec,tx_sent,amount_sent,balance,uniques,sibling' --local -upool -ppool db /root/behaviour/gen.csv