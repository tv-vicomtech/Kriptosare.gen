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

    time.sleep(5)
    mining_blocks(client,nodelist[0],"btc",100)
    time.sleep(5)
    mining_blocks(client,nodelist[0],"btc",100)
    time.sleep(5)
    nodelist_pool= get_containers_names(client, DOCK_IMAGE_NAME_POOL+".")
    nodelist_all=nodelist+nodelist_pool
    for i in range(0,5):
	    send_money_to_all(client,nodelist[0],nodelist_all,"btc")
	    time.sleep(5)
    numblock = rpc_call(client, nodelist[0], 'getblockcount')

    print("**************************************")
    print("NETWORK STATISTICS")
    print("Actual Block height: " + str(numblock))
    for i in range(0,len(nodelist_all)):
    	print("node: " + str(nodelist_all[i])+" balance: "+ str(rpc_call(client, nodelist_all[i], 'getbalance')))

    print("ENVIRONMENT READY!")
    #howmanyblock=100
    #generaterandomtransaction(client,nodelist,"btc",howmanyblock)
    