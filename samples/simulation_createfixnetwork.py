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
        client.images.build(path="../exchange", tag=DOCK_IMAGE_NAME_EX)
        client.images.build(path="../casino", tag=DOCK_IMAGE_NAME_CAS)
        client.images.build(path="../pool", tag=DOCK_IMAGE_NAME_POOL)
        client.images.build(path="../mixer", tag=DOCK_IMAGE_NAME_MXR)

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
    G= nx.read_graphml('../graphml/model/model4_400.graphml', unicode)

    nodelist=[]
    print "***************************"
    print "*********CREATE CONTAINERS************"
    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
    number_mx = 13
    number=len(G.nodes)-number_mx

    #create_node(client, DOCK_NETWORK_NAME_BTC, "btc", number)
    create_behvnode(client, number_mx, DOCK_IMAGE_NAME_MXR, DOCK_IMAGE_NAME_MXR) #mixer

    print "Containers created"
    nodelist = get_containers_names(client, fixname)
    time.sleep(10)
    for x in G.edges:
        a = int(x[0])
        if(a<number_mx):
            radix=DOCK_CONTAINER_NAME_PREFIX_MXR+"."+str(a+1)
        else:
            radix=fixname+str(a-number_mx+1)


        source=radix

        b = int(x[1])
        if(b<number_mx):
            radix=DOCK_CONTAINER_NAME_PREFIX_MXR+"."+str(b+1)
        else:
            radix=fixname+str(b-number_mx+1)

        destination=radix

        print "connect "+source +" to "+destination
        r = rpc_create_connection(client, source,destination,"btc")    
    print "End Connections"
    