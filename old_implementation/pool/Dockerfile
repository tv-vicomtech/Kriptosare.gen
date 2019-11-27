FROM effezeta88/btc

RUN apt-get update
RUN apt-get install -y python python-dev libmysqlclient-dev
RUN apt-get install -y python-pip
RUN pip install python-bitcoinrpc docker==2.7.0 mysqlclient numpy

RUN { \
        echo mysql-community-server mysql-community-server/data-dir select '/var/lib/mysql'; \
        echo mysql-community-server mysql-community-server/root-pass password 'password'; \
        echo mysql-community-server mysql-community-server/re-root-pass password 'password'; \
        echo mysql-community-server mysql-community-server/remove-test-db select false; \
    } | debconf-set-selections \
    && apt-get update && apt-get install -y mysql-server

RUN mkdir /root/lib/
RUN mkdir /root/behaviour/

ADD bitcoin.conf /root/.bitcoin/
ADD behaviour/* /root/behaviour/
ADD script.sh /etc/init.d/
ADD insert_sql.sh /etc/init.d/
ADD script_zch.sh /etc/init.d/
ADD lib/* /root/lib/




