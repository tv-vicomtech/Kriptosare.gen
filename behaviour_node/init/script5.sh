#!/bin/bash
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

sed -i '42 a  innodb_use_native_aio = 0' /etc/mysql/my.cnf
sleep 10

/etc/init.d/mysql start
sleep 5

PASS="vicom"
mysql -uroot <<MYSQL_SCRIPT
CREATE DATABASE db;
CREATE USER 'vicom'@'localhost' IDENTIFIED BY '$PASS';
GRANT ALL PRIVILEGES ON db.* TO 'vicom'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

mysql -uroot <<MYSQL_SCRIPT
USE db;
DROP TABLE IF EXISTS received_tx;
CREATE TABLE received_tx(
    idrecv INT(32) NOT NULL AUTO_INCREMENT,
    source VARCHAR(20),
    destination VARCHAR(45),
    currencies VARCHAR(5),
    amount VARCHAR(10),
    confirmations INT(2),
    blk INT(6),
    time DATETIME,
    
    PRIMARY KEY (idrecv)
);

DROP TABLE IF EXISTS synthetic;
CREATE TABLE synthetic(
    idgen INT(32) NOT NULL AUTO_INCREMENT,
    tx_rec INT(10),
    amount_rec VARCHAR(8),
    tx_sent INT(10),
    amount_sent VARCHAR(8),
    balance VARCHAR(8),
    uniques INT(2),
    sibling INT(6),
    
    PRIMARY KEY (idgen)
);

CREATE TABLE user(
    iduser INT(32) NOT NULL AUTO_INCREMENT,
    IP VARCHAR(16),
    PRIMARY KEY (iduser)
);

DROP TABLE IF EXISTS transaction;
CREATE TABLE transaction(
    idtx INT(32) NOT NULL AUTO_INCREMENT,
    address VARCHAR(45),
    tx_rec INT(10),
    amount_rec VARCHAR(8),
    tx_sent INT(10),
    amount_sent VARCHAR(8),
    balance VARCHAR(8),
    uniques INT(2),
    sibling INT(6),
    idgen INT(32),

    PRIMARY KEY (idtx)
);
MYSQL_SCRIPT

bitcoind -datadir=/root/.bitcoin/ &

sleep 5

mysqlimport --fields-terminated-by=, --columns='tx_rec,amount_rec,tx_sent,amount_sent,balance,uniques,sibling' --local -uvicom -pvicom db /root/behaviour/mixer/synthetic.csv


sleep 10
nohup python /root/lib/scanning.py & > /root/lib/log/log.scanning.txt
nohup python /root/lib/listener_address.py & > /root/lib/log/log.listeneraddress.txt
nohup python /root/lib/resend.py & > /root/lib/log/log.resend.txt
nohup python /root/lib/listener.py 
