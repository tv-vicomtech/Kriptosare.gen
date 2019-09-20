FROM ubuntu:14.04

RUN apt-get -y update
RUN apt-get install -y wget net-tools git python3-dev python3-pip curl apt-transport-https
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:webupd8team/java
RUN apt-get -y update
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections \
&& apt-get install -y oracle-java8-installer


RUN pip3 install requests==2.13.0 cassandra-driver

RUN echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list
RUN curl https://www.apache.org/dist/cassandra/KEYS | apt-key add -
#RUN apt-key adv --keyserver pool.sks-keyservers.net --recv-key A278B781FE4B2BDA

RUN apt-get update
RUN apt-get install -y cassandra
RUN apt-get install -y jq

RUN cd /opt/ && git clone https://github.com/graphsense/graphsense-datafeed.git

RUN cd /opt/ && git clone https://github.com/graphsense/graphsense-transformation.git

# Installation of scala
RUN apt-get -f install
RUN apt-get -y install scala

# Installation of sbt
RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
RUN apt-get update
RUN apt-get -y install sbt

RUN cd /opt/ && wget http://apache.uib.no/spark/spark-2.2.2/spark-2.2.2-bin-hadoop2.7.tgz && tar -xvzf spark-2.2.2-bin-hadoop2.7.tgz
RUN cd /opt/spark-2.2.2-bin-hadoop2.7
RUN mv /opt/spark-2.2.2-bin-hadoop2.7 /usr/local/
RUN ln -s /usr/local/spark-2.2.2-bin-hadoop2.7/ /usr/local/spark
RUN cd /usr/local/spark && /usr/local/spark/sbin/start-master.sh
RUN /usr/local/spark/sbin/start-slave.sh spark://ethane:7077

RUN cd /opt/ && git clone https://github.com/sbt/sbteclipse.git

ADD data-transformation/plugins.sbt /opt/graphsense-transformation/project
ADD data-transformation/schema_transformed.cql /opt/graphsense-transformation/
ADD data-transformation/ait/* /opt/graphsense-transformation/src/main/scala/at/ac/ait/


RUN cd /opt/graphsense-transformation && sbt eclipse

ADD datafeed/* /opt/graphsense-datafeed/

ADD script.sh /etc/init.d/
ADD script2.sh /etc/init.d/
ADD script20.sh /etc/init.d/
ADD script21.sh /etc/init.d/
ADD copy_cassandra_to_csv.sh /root/

ENV SPARK_HOME=/usr/local/spark

EXPOSE 7000 7001 7199 9000 9042 9160 4040

