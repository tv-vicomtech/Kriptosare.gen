FROM effezeta88/blocksci

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install jupyter

# Copy bitcoin.conf to the container
ADD bitcoin.conf /root/.bitcoin/
ADD script.sh /etc/init.d/
ADD script_zch.sh /etc/init.d/
ADD notebooks/* /opt/BlockSci/Notebooks/
