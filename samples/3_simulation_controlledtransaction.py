import sys

sys.path.insert(0, '../python_mod')

from docker_utils import *
from multirawtransaction import *
from btcconf import *
from rpc_utils import *
from connection import *
from decimal import *

import logging
from random import randint, random
import time
from getopt import getopt
from mysocket import *
from sendlib import *


if __name__ == '__main__':

    if len(argv) > 1:
        # Get params from call
        _, args = getopt(argv, ['nobuild', 'nonet'])
        build = False if '--nobuild' in args else True
        network = False if '--nonet' in args else True
        remove = False if '--noremove' in args else True
    else:
        build = True
        network = True
        remove = True

    # Create docker client & network
    #client = docker_setup(build_image=build, create_docker_network=network, remove_existing=remove)
    client = docker.from_env()


    nodelist = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")  

    nodelist_pool= get_containers_names(client, DOCK_IMAGE_NAME_POOL+".")
    nodelist_ex = get_containers_names(client, DOCK_IMAGE_NAME_EX+".")
    nodelist_gam = get_containers_names(client, DOCK_IMAGE_NAME_CAS+".")
    nodelist_mrk = get_containers_names(client, DOCK_IMAGE_NAME_MRK+".")
    nodelist_mxr = get_containers_names(client, DOCK_IMAGE_NAME_MXR+".")
    nodelist_ser = get_containers_names(client, DOCK_IMAGE_NAME_SER+".")

    nodelist_behavioural=nodelist_pool+ nodelist_ex+nodelist_gam+nodelist_mrk+nodelist_mxr+nodelist_ser
    nodelist_all=nodelist+nodelist_behavioural
    
    ########################################################################
    # Behavioural transaction
    ########################################################################
    print("**********************************")
    print("Transaction START!")
    hh = randint(0,len(nodelist_behavioural)-1)
    destination_node=nodelist_behavioural[hh]
    json_transaction= ask_address(client,destination_node)
    json_transaction = json_transaction.decode('utf-8')
    json_transaction = json.loads(json_transaction)

    destination_addr=json_transaction["address"]
    num_tx = json_transaction["tx"]
    amount = json_transaction["amount"]

    hh = randint(0,len(nodelist)-1)

    source=nodelist[hh]
    balance= rpc_call(client, source, 'getbalance')
    
    if(balance>=float(amount)):
        amount_to_send = round(float(amount)/int(num_tx),8)
    else:
        amount_to_send = round(float(balance)/int(num_tx),8)

    if(amount_to_send>0.001):
        for i in range(0,int(num_tx)):
            print(str(i)+") from: "+source+" to "+destination_node+" ("+destination_addr+") "+str(amount_to_send))
            send_to_node(client,source,destination_addr,"btc",amount_to_send,datetime.datetime.now(),destination_node)
            send_to_address(client,source,amount_to_send,destination_addr,"btc",False)
        
        print("Transaction END!")
    else:
        print("Not enough money...try later...END!")
    #mining_blocks(client,nodelist[0],"btc",1)    
    print("****************************************")
