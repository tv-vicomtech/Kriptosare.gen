FROM effezeta88/btc_sql

ADD script.sh /etc/init.d/
ADD script_import.sh /etc/init.d/
ADD lib/* /root/lib/

# Copy bitcoin.conf to the container
ADD bitcoin.conf /root/.bitcoin/

