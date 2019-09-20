FROM effezeta88/btc

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server=5.7.22 \
 && rm -rf /var/lib/mysql \
&& rm -rf /var/lib/apt/lists/*

COPY listener.py /home/exchange
COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /home/exchange/listener.py
RUN chmod 755 /sbin/entrypoint.sh

ENTRYPOINT ["/sbin/entrypoint.sh"]
# Copy bitcoin.conf to the container
ADD --chown=bitcoin:bitcoin bitcoin.conf /home/bitcoin/.bitcoin/
ADD --chown=bitcoin:bitcoin table.sql /home/bitcoin/
ADD --chown=bitcoin:bitcoin listener.py /home/bitcoin/



