FROM debian:8
LABEL maintainer=mihai.bartha@ait.ac.at

################## BEGIN INSTALLATION ######################
RUN apt-get update --fix-missing && \
    apt-get install -y python3 python3-pip nginx upstart net-tools
RUN pip3 install --upgrade pip
RUN mkdir -p /srv/graphsense-dashboard
ADD ./requirements.txt /srv/graphsense-dashboard
RUN cd /srv/graphsense-dashboard; pip3 install -r requirements.txt
ADD ./ /srv/graphsense-dashboard/
# connect dashboard to docker bridge network
ADD ./uwsgi /etc/init.d/uwsgi
ADD ./dashboard /etc/nginx/sites-available/dashboard
RUN ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled
RUN rm /etc/nginx/sites-enabled/default
ADD script.sh /etc/init.d/
ADD script_zch.sh /etc/init.d/
##################### INSTALLATION END #####################
