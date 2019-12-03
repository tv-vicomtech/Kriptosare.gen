FROM effezeta88/datafeed_collector

RUN mkdir /root/.bitcoin
ADD datafeed/* /opt/graphsense-datafeed/
ADD script.sh /etc/init.d/
ADD script2.sh /etc/init.d/
ADD script2_lite.sh /etc/init.d/

ENV SPARK_HOME=/usr/local/spark

EXPOSE 7000 7001 7199 9000 9042 9160 4040

