# Use the official Ubuntu 14.04 as a parent image.
FROM ubuntu:14.04

# Update the package list and install software properties common.
RUN apt-get update && apt-get install -y software-properties-common

# Add bitcoind from the official PPA
RUN add-apt-repository --yes ppa:bitcoin/bitcoin && LC_ALL=C.UTF-8 add-apt-repository --yes ppa:ondrej/php && apt-get update

# Install bitcoind and make
RUN apt-get install -y bitcoind make

# Install additional packages
RUN apt-get -y update
RUN apt-get purge php5-common -y

# dependencies
RUN apt-get -y install vim\
 python-dev\
 python-flup\
 python-pip\
 expect\
 git\
 wget\
 netcat\
 net-tools\
 pkg-config\
 nodejs\
 libmysqlclient-dev\
 apache2

RUN chmod 777 /tmp
RUN apt-get install -y debconf-utils \
    && echo mysql-server-5.5 mysql-server/root_password password password | debconf-set-selections \
    && echo mysql-server-5.5 mysql-server/root_password_again password password | debconf-set-selections \
    && apt-get install -y mysql-server\
    && rm -rf /var/lib/apt/lists/*
    
RUN apt-get -y update

RUN apt-get -y install php7.0 php-mysql php7.0-dev libapache2-mod-php php7.0-mcrypt

RUN pip install json-rpc\
 python-bitcoinrpc\
 mysql-python==1.2.5\ 
 mysqlclient\
 docker-py\
 networkx

RUN useradd -d /home/bitcoin -m -s /bin/bash -c "bitcoin" -p `openssl passwd -1 bitcoin` bitcoin
RUN apt-get install -y sudo
RUN echo "bitcoin ALL=(ALL) ALL" >> /etc/sudoers

# Copy bitcoin.conf to the container
ADD --chown=bitcoin:bitcoin db/mysql-table-creation.sql /home/bitcoin/db/
ADD --chown=bitcoin:bitcoin mixer/* /home/bitcoin/mixer/
ADD --chown=bitcoin:bitcoin init.sql /home/bitcoin/
ADD --chown=bitcoin:bitcoin service-up.sh /home/bitcoin/
ADD --chown=bitcoin:bitcoin insert_addr.sh /home/bitcoin/
ADD www/* /var/www/html/
ADD --chown=bitcoin:bitcoin bitcoin.conf /home/bitcoin/.bitcoin/

# Set the working directory
WORKDIR /home/bitcoin

# Export port 18332 (see bitcoin.conf)
EXPOSE 18332 80 3306



