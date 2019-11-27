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
RUN mkdir /root/lib/log
RUN mkdir /root/behaviour/
RUN mkdir /root/behaviour/exchange
RUN mkdir /root/behaviour/gambling
RUN mkdir /root/behaviour/market
RUN mkdir /root/behaviour/mixer
RUN mkdir /root/behaviour/pool
RUN mkdir /root/behaviour/service

ADD bitcoin.conf /root/.bitcoin/

ADD behaviour/exchange/* /root/behaviour/exchange/
ADD behaviour/gambling/* /root/behaviour/gambling/
ADD behaviour/market/* /root/behaviour/market/
ADD behaviour/mixer/* /root/behaviour/mixer/
ADD behaviour/pool/* /root/behaviour/pool/
ADD behaviour/service/* /root/behaviour/service/

ADD init/* /etc/init.d/
ADD lib/* /root/lib/




