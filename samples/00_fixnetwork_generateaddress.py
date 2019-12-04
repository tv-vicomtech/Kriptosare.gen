import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *

import logging
from random import randint
import time
import datetime
from getopt import getopt
from mysocket import *

def tool_bar(tt):
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * tt))
    sys.stdout.flush()
    sys.stdout.write("\b" * (tt+1)) # return to start of line, after '['

    for i in range(tt):
        time.sleep(1) # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n") # this ends the progress bar

def starting_generator(client):
    containers = client.containers.list()
    for uuid in containers:
        uuid.exec_run("python /root/lib/generate_destination.py &",detach=True)


def docker_setup(build_image=True, create_docker_network=True, remove_existing=True):
    """
    Creates the docker client and optionally:
        - builds docker image
        - creates docker network
        - removes containers from previous deployments

    :param build_image: boolean, whether to build the image
    :param create_docker_network: boolean, whether to create the docker network
    :param remove_existing: boolean, whether to remove already existing containers
    :return: docker client
    """

    client = docker.from_env()
    if build_image:
        client.images.build(path="../btc_testbed", tag=DOCK_IMAGE_NAME_BTC)
        client.images.build(path="../behaviour_node", tag=DOCK_IMAGE_NAME_BEH)
 

    if create_docker_network:
        create_network(client)
    if remove_existing:
        remove_containers(client)
    return client

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

    client = docker_setup(build_image=True, create_docker_network=False, remove_existing=False)
    G= nx.read_graphml('../graphml/model/model0_250.graphml')

    nodelist=[]
    print("***************************")
    print("*********CREATE CONTAINERS************")
    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."

    number_pool = 0
    number_ex = 0
    number_cas = 0
    number_mrk = 0
    number_mxr = 0
    number_ser = 0
    number=len(G.nodes) - number_pool - number_ser - number_ex - number_mrk - number_cas - number_mxr
    
    block_container=10
    modul=number//block_container
    print(datetime.datetime.now())
    for i in range(0,modul):
        create_node_nocmd(client, DOCK_NETWORK_NAME_BTC, i*block_container, (i+1)*block_container)

    rest=number-(modul*block_container)
    if(rest!=0):
        create_node_nocmd(client, DOCK_NETWORK_NAME_BTC, modul*block_container,number)

    if(number_ex>0):
        create_behvnode_gan(client, number_ex, 1, DOCK_CONTAINER_NAME_PREFIX_EX) #mixer
    if(number_cas>0):
        create_behvnode_gan(client, number_cas, 2, DOCK_CONTAINER_NAME_PREFIX_CAS) #mixer
    if(number_mrk>0):
        create_behvnode_gan(client, number_mrk, 3, DOCK_CONTAINER_NAME_PREFIX_MRK) #mixer
    if(number_pool>0):
        create_behvnode_gan(client, number_pool, 4, DOCK_CONTAINER_NAME_PREFIX_POOL) #mixer
    if(number_mxr>0):
        create_behvnode_gan(client, number_mxr, 5, DOCK_CONTAINER_NAME_PREFIX_MXR) #mixer
    if(number_ser>0):
        create_behvnode_gan(client, number_ser, 6, DOCK_CONTAINER_NAME_PREFIX_SER) #mixer

    print(datetime.datetime.now())
    print("Containers created")
    print("Wait 300 seconds...")
    tool_bar(300)
    print("End!")
