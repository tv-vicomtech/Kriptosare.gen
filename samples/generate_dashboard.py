import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *

import logging
import time
from getopt import getopt
from random import randint
from decimal import Decimal


def create_machine(client):
    """
    Creates a network with the topology extracted from a graph.

    Warning: remember to call docker_setup with remove_existing=True or to set the names of the nodes so that they
    do not overlap with existing ones.

    :param client: docker client
    :param g: networkx graph
    :return:
    """

	
    generate_dock_statoshi(client)
    generate_dock_blocksci(client)

    time.sleep(5)
    nodelist=[]
    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
    nodelist=get_containers_names(client, fixname)

    ######################STATOSHI CONNECTIONS ARE GENERATE DYNAMICALLY (RANDOM)#########################
    nodes_name_statoshi=client.containers.list(filters={'name': 'btc_statoshi'})
    random_connection_element(client,nodelist,nodes_name_statoshi[0].name,fixname,"btc")

    ######################BLOCKSCI CONNECTIONS ARE GENERATE DYNAMICALLY (RANDOM)#########################
    nodes_name_blocksci=client.containers.list(filters={'name': 'btc_blocksci'})
    random_connection_element(client,nodelist,nodes_name_blocksci[0].name,fixname,"btc")

    return



def rand_list(nodelist,n_):
    answ=[]
    for idx in range(0,n_):
        r=randint(0,len(nodelist)-1)
        if(nodelist[r] not in answ):
            answ.append(nodelist[r])
        else:
            idx=idx-1
    return answ

def docker_setup(build_image, remove_existing):
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
	print(" ********blocksci*****")
        client.images.build(path="../blocksci", tag=DOCK_IMAGE_NAME_BLOCKSCI)
	print(" ********statoshi*****")
        client.images.build(path="../statoshi", tag=DOCK_IMAGE_NAME_STATOSHI)

    if remove_existing:
	for i in range(0,len(nodes_name)):
		remove_container_by_name(client,nodes_name[i].name)
	nodes_name=client.containers.list(filters={'name': DOCK_IMAGE_NAME_STATOSHI})
	for i in range(0,len(nodes_name)):
		remove_container_by_name(client,nodes_name[i].name)
        nodes_name=client.containers.list(filters={'name': DOCK_MACHINE_NAME_BLOCKSCI_BTC})
	for i in range(0,len(nodes_name)):
		remove_container_by_name(client,nodes_name[i].name)
    return client


if __name__ == '__main__':

    net=False
    # Create docker client & network
    client = docker_setup(True,True)

    net=retrive_network(client,DOCK_NETWORK_NAME_BTC)
    if(net):
    	create_machine(client)
    else:
	    print "No network interface"

    print "*****OK*****"

