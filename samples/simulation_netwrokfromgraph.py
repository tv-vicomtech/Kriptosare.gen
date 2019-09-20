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

    G= nx.read_graphml('../graphml/graph_example.graphml', unicode)

    client = docker_setup(build_image=build, create_docker_network=network, remove_existing=remove)
 
    nodelist=[]
    print "***************************"
    print "*********CREATE CONTAINERS************"

    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
    number=len(G.nodes)
    create_node(client, DOCK_NETWORK_NAME_BTC, "btc", number) 

    print "Containers created"
    time.sleep(15)
    nodelist = get_containers_names(client, fixname)
    connection_from_graph(client,G,nodelist,fixname,"btc")
    #random_connection_container_graph(client,G,nodelist,fixname,"btc", 8)
    print "End Connections"
    #print "Total: "+str(len(nodelist))+" nodes"
    f=plt.figure()
    pos = nx.spring_layout(G,k=0.15,iterations=20)
    nx.draw(G,pos,with_labels = True)
    f.savefig("../graphml/simple_path.png") # save as png
    #plt.show()
    print "Done"
