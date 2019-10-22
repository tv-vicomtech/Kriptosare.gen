#!/bin/bash
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

sed -i '42 a  innodb_use_native_aio = 0' /etc/mysql/my.cnf
sleep 10

/etc/init.d/mysql start
sleep 5

PASS="pool"
mysql -uroot <<MYSQL_SCRIPT
CREATE DATABASE db;
CREATE USER 'pool'@'localhost' IDENTIFIED BY '$PASS';
GRANT ALL PRIVILEGES ON db.* TO 'pool'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

mysql -uroot <<MYSQL_SCRIPT
USE db;
DROP TABLE IF EXISTS pool;
CREATE TABLE pool(
    idpo INT(32) NOT NULL AUTO_INCREMENT,
    source VARCHAR(20),
    currencies VARCHAR(5),
    amount VARCHAR(10),
    confirmations INT(2),
    blk INT(6),
    time DATETIME,
    
    PRIMARY KEY (idpo)
);

DROP TABLE IF EXISTS gen;
CREATE TABLE gen(
    idgen INT(32) NOT NULL AUTO_INCREMENT,
    tx_rec INT(32),
    amount_rec VARCHAR(8),
    tx_sent INT(10),
    amount_sent VARCHAR(8),
    balance VARCHAR(8),
    uniques INT(2),
    sibling INT(6),
    
    PRIMARY KEY (idgen)
);

DROP TABLE IF EXISTS transaction;
CREATE TABLE transaction(
    idtx INT(32) NOT NULL AUTO_INCREMENT,
    tx_rec INT(32),
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
bash /etc/init.d/insert_sql.sh

sleep 10
nohup python /root/lib/listener.py > list.txt &
nohup python /root/lib/resend.py
