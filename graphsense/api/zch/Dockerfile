FROM ubuntu:14.04

RUN apt-get -y update
RUN apt-get install -y wget net-tools git python3-dev python3-pip curl apt-transport-https
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:webupd8team/java
RUN apt-get -y update
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections \
&& apt-get install -y oracle-java8-installer

RUN apt-get update

# Installation of scala
RUN apt-get -f install
RUN apt-get -y install scala

# Installation of sbt
RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
RUN apt-get update
RUN apt-get -y install sbt


RUN cd /opt/ && git clone https://github.com/graphsense/graphsense-REST.git
ADD rest-api/application.conf /opt/graphsense-REST/conf
ADD rest-api/plugins.sbt /opt/graphsense-REST/project
ADD rest-api/Model.scala /opt/graphsense-REST/app/models/

RUN cd /opt/ && git clone https://github.com/sbt/sbteclipse.git

RUN cd /opt/graphsense-REST && sbt eclipse && sbt clean stage

ADD script.sh /etc/init.d/
ADD script_restart.sh /etc/init.d/

EXPOSE 7000 7001 7199 9000 9042 9160 4040

