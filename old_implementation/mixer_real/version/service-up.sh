#!/bin/bash
chmod 644 /usr/lib/sudo/sudoers.so
chown -R root /usr/lib/sudo
ip=$(ifconfig eth0 2>/dev/null |awk '/inet addr:/ {print $2}'|sed 's/addr://')
echo "ServerName" $ip >> /etc/apache2/apache2.conf
service apache2 start
chmod -R 775 /etc/mysql/
service mysql start
cat init.sql | mysql -u root -ppassword
mysql -u vicomtech -pvicomtech  db  < /home/bitcoin/db/mysql-table-creation.sql
cd /home/bitcoin/
sudo su bitcoin << EOF
./insert_addr.sh &
EOF
bitcoind -datadir=/home/bitcoin/.bitcoin/

