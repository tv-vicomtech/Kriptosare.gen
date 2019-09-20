FROM effezeta88/btc

RUN apt-get update
RUN apt-get install -y python-dev libmysqlclient-dev
RUN apt-get install -y python-pip
RUN pip install python-bitcoinrpc docker==2.7.0 mysqlclient numpy

RUN { \
        echo mysql-community-server mysql-community-server/data-dir select '/var/lib/mysql'; \
        echo mysql-community-server mysql-community-server/root-pass password 'password'; \
        echo mysql-community-server mysql-community-server/re-root-pass password 'password'; \
        echo mysql-community-server mysql-community-server/remove-test-db select false; \
    } | debconf-set-selections \
    && apt-get update && apt-get install -y mysql-server
	
EXPOSE 18332 

RUN mkdir /root/lib/

ADD bitcoin.conf /root/.bitcoin/
ADD script.sh /etc/init.d/
ADD lib/* /root/lib/










