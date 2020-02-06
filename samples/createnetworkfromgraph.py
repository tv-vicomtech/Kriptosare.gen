import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging
from random import randint
import time
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

    G= nx.read_graphml('../graphml/model/model0_10.graphml')

    client = docker_setup(build_image=build, create_docker_network=network, remove_existing=remove)
 
    nodelist=[]
    print("***************************")
    print("*********CREATE CONTAINERS************")

    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
    number=len(G.nodes)

    number_pool = 1
    number_ex = 1
    number_cas = 1
    number_mrk = 1
    number_mxr = 1
    number_ser = 1
    number=len(G.nodes) - number_pool - number_ser - number_ex - number_mrk - number_cas - number_mxr

    create_node_import(client, DOCK_NETWORK_NAME_BTC, "btc", number)

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


    print("Containers created")
    tool_bar(120)

    print("Start connection")
    connection_from_graph(client,G,nodelist,fixname,"btc",number_ex,number_cas,number_mrk,number_pool,number_mxr,number_ser)
    print("***************************")
    #plt.show()
    print("Done")
