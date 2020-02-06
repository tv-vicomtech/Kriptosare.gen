#Example of operations with mixers 
#This script should be used after btc network and btc mixer SERVICES are created
import sys

sys.path.insert(0, '../python_mod')

from rpc_utils import *
from docker_utils import *
from multirawtransaction import *

from conf import *
import logging
import time
import json
from sys import argv
from getopt import getopt
from random import randint
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

    logging.info('Setting up docker client')
    client = docker.from_env()
    if build_image:
        logging.info("  Building docker image")
        client.images.build(path="btc_testbed", tag=DOCK_IMAGE_NAME)
        #client.images.build(path="btc_mixer", tag=DOCK_IMAGE_NAME_MIXER)
    if create_docker_network:
        logging.info("  Creating network")
        create_network(client)
    if remove_existing:
        logging.info("  Removing existing containers")
        service_list=client.services.list(filters={'name': 'btc'})
        for element in service_list:
            element.remove()
        service_list=client.services.list(filters={'name': 'btc_mixer'})
        for element in service_list:
            element.remove()

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

    create_node(client, DOCK_NETWORK_NAME_BTC, "btc", 10) 
    time.sleep(5)
    create_new_mixer_service(client,1)

    random_connection_container(client,"btc", 4)

    nodes_name=client.containers.list(filters={'status':'running','ancestor': 'btc'})
    nodes_name_mixer=client.containers.list(filters={'status':'running','ancestor': 'btc_mixer'})

    time.sleep(5)

    nodes_name_mixers=client.containers.list(filters={'ancestor': 'btc_mixer'})

    random_connection_service(client,nodes_name,nodes_name_mixers,5)

    nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")  
    time.sleep(5)
    mining_blocks(client,nodelist[0],"btc",101)
    time.sleep(5)
    send_money_to_all(client,nodelist,"btc")
    time.sleep(5)

    source_addr = rpc_call(client, nodelist[0], 'getaccountaddress', '""')

    destination_addr = rpc_call(client, nodelist[1], 'getaccountaddress', '""')

    source_addr2 = rpc_call(client, nodelist[3], 'getaccountaddress', '""')

    destination_addr2 = rpc_call(client, nodelist[4], 'getaccountaddress', '""')

    ip_mixer=get_ip_by_unknown(client,nodes_name_mixer[0].name)

    velocity = "1" #1 for fast mas delay 2 for delay

    mixer_addr=send_request(client,ip_mixer,source_addr,destination_addr,velocity)
    mixer_addr2=send_request(client,ip_mixer,source_addr2,destination_addr2,velocity)

    if(mixer_addr!=-1):
        time.sleep(30)
        print "******Sending to Mixer*****"
        rpc_call(client, nodelist[0], 'sendtoaddress', "'" +mixer_addr+ "','1'")
        rpc_call(client, nodelist[3], 'sendtoaddress', "'" +mixer_addr2+ "','1'")
        for i in range(0,7):
            print "******Mining a new block*****"
            time.sleep(30)
            rpc_call(client, nodelist[1], 'generate', '1')
        numblock = rpc_call(client, nodelist[0], 'getblockcount')
        print "Block height: " + str(numblock)

    print "*****END*****"
