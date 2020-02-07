#!/bin/bash
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

sed -i '42 a  innodb_use_native_aio = 0' /etc/mysql/my.cnf
sed -i 's/bind-address.*/bind-address = 0.0.0.0/g' /etc/mysql/my.cnf
sleep 10

/etc/init.d/mysql start
sleep 5

PASS="vicom"
mysql -uroot <<MYSQL_SCRIPT
CREATE DATABASE db;
CREATE USER 'vicom'@'%' IDENTIFIED BY '$PASS';
GRANT ALL PRIVILEGES ON db.* TO 'vicom'@'%';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

mysql -uroot <<MYSQL_SCRIPT
USE db;

CREATE TABLE destination(
    iddest INT(32) NOT NULL AUTO_INCREMENT,
    address VARCHAR(45),
    IP VARCHAR(16),
    PRIMARY KEY (iddest)
);
MYSQL_SCRIPT

#nohup python /root/lib/generate_destination.py & > log.generate.txt

bitcoind -datadir=/root/.bitcoin/ 


