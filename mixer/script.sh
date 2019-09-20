#!/bin/bash
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

sed -i '42 a  innodb_use_native_aio = 0' /etc/mysql/my.cnf

/etc/init.d/mysql start
sleep 10

PASS="mixer"
mysql -uroot <<MYSQL_SCRIPT
CREATE DATABASE db;
CREATE USER 'mixer'@'localhost' IDENTIFIED BY '$PASS';
GRANT ALL PRIVILEGES ON db.* TO 'mixer'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

mysql -uroot <<MYSQL_SCRIPT
USE db;
DROP TABLE IF EXISTS mixer;
CREATE TABLE mixer(
    idmix INT(32) NOT NULL AUTO_INCREMENT,
    source VARCHAR(20),
    address_in VARCHAR(50),
    destination VARCHAR(50),
    amount VARCHAR(10),
    confirmations INT(2),
    deadline INT(2),
    blk INT(6),
    time DATETIME,
    
    PRIMARY KEY (idmix)
);
MYSQL_SCRIPT

bitcoind -datadir=/root/.bitcoin/ &
sleep 10
nohup python /root/lib/listener.py > list.txt 
#nohup python /root/lib/resend.py
