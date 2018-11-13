FROM effezeta88/btc_statoshi

ADD my_script.sh /etc/init.d/
ADD bitcoin.conf /root/.bitcoin/
RUN chmod 775 /etc/init.d/my_script.sh

# defaults
EXPOSE 82 3000 2003-2004 2023-2024 8125 8125/udp 8126 18332

