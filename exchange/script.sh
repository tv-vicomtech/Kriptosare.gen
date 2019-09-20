#!/bin/bash
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

sed -i '42 a  innodb_use_native_aio = 0' /etc/mysql/my.cnf

/etc/init.d/mysql start
sleep 5

PASS="exchange"
mysql -uroot <<MYSQL_SCRIPT
CREATE DATABASE db;
CREATE USER 'exchange'@'localhost' IDENTIFIED BY '$PASS';
GRANT ALL PRIVILEGES ON db.* TO 'exchange'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

mysql -uroot <<MYSQL_SCRIPT
USE db;
DROP TABLE IF EXISTS exchange;
CREATE TABLE exchange(
    idex INT(32) NOT NULL AUTO_INCREMENT,
    source VARCHAR(20),
    destination VARCHAR(50),
    fromcurrencies VARCHAR(5),
    tocurrencies VARCHAR(5),
    amount VARCHAR(10),
    confirmations INT(2),
    blk INT(6),
    time DATETIME,
    
    PRIMARY KEY (idex)
);
MYSQL_SCRIPT

bitcoind -datadir=/root/.bitcoin/ -rpcport=18332 &

#/root/zcash/src/zcashd -datadir=/root/.zcash &
sleep 5
nohup python /root/lib/listener.py > list.txt &
nohup python /root/lib/resend.py
