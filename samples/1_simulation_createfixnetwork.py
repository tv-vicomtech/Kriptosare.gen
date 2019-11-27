import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *

import logging
from random import randint
import time
from getopt import getopt
from mysocket import *


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
    G= nx.read_graphml('../graphml/model/model0_10.graphml')

    nodelist=[]
    print("***************************")
    print("*********CREATE CONTAINERS************")
    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
    number_pool = 3
    number=len(G.nodes)-number_pool

    create_node(client, DOCK_NETWORK_NAME_BTC, "btc", number)
    #create_behvnode_gan(client, number_pool, 1, DOCK_CONTAINER_NAME_PREFIX_EX) #mixer
    #create_behvnode_gan(client, number_pool, 2, DOCK_CONTAINER_NAME_PREFIX_CAS) #mixer
    #create_behvnode_gan(client, number_pool, 3, DOCK_CONTAINER_NAME_PREFIX_MRK) #mixer
    create_behvnode_gan(client, number_pool, 4, DOCK_CONTAINER_NAME_PREFIX_POOL) #mixer
    #create_behvnode_gan(client, number_pool, 5, DOCK_CONTAINER_NAME_PREFIX_MXR) #mixer
    #create_behvnode_gan(client, number_pool, 6, DOCK_CONTAINER_NAME_PREFIX_SER) #mixer


    print("Containers created")
    time.sleep(90)
    nodelist = get_containers_names(client, fixname)
    connection_from_graph(client,G,nodelist,fixname,"btc",0,0,0,0,number_pool,0)
    print("End Connections")
    