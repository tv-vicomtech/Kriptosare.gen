import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *
import logging
import time

import os 

if __name__ == '__main__':

    client = docker.from_env()

    nodelist=[]
    print("***************************")
    print("*********Extraction data************")

    nodelist = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")

    for i in range(0, len(nodelist)):
        os.system('docker cp '+nodelist[i]+':/address.csv  /home/titanium/Kriptosare.gen/backupwallet/address'+str(i)+'.csv') 
        os.system('docker cp '+nodelist[i]+':/walletdump  /home/titanium/Kriptosare.gen/backupwallet/walletdump'+str(i)) 

    print("*********END!************")
