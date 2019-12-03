import sys
import docker
import time
from getopt import getopt
from random import randint
from decimal import Decimal
import sys
sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *

def collector_setup():


    client = docker.from_env()
    print(" ********datafeed*****")
    client.images.build(path="../collector/data", tag="datafeed")

    return client

def generate_collector(client):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    containers = client.containers
    print("probe")

    CMD = "bitcoind -rest -datadir=/root/.bitcoin"
    containers.run(
        DOCK_IMAGE_NAME_BTC,
        CMD,
        name="bitcoin_probe",
        detach=True,
        network=DOCK_NETWORK_NAME_BTC)

    
    CMD = "/etc/init.d/script.sh"
    port = {'9042':9042}

    print("DATAFEED")
    containers.run(
        "datafeed",
        CMD,
        name="datafeed_regtest",
        detach=True,
        network=DOCK_NETWORK_NAME_BTC,
        ports=port)

if __name__ == '__main__':

    client = collector_setup()
    generate_collector(client)
    time.sleep(10)

    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
    fixname_data="bitcoin_probe"

    nodelist = get_containers_names(client, fixname)
    nodelist_data = get_containers_names(client, fixname_data)
    cryptomoney="btc"
    source=nodelist_data[0]
    
    time.sleep(10)

    print("connection "+str(source)+ " to "+ str(nodelist[0]))
    r = rpc_create_connection(client, source, nodelist[0],cryptomoney)
    print("connection "+str(source)+ " to "+ str(nodelist[1]))
    r = rpc_create_connection(client, source,nodelist[1],cryptomoney)
    print("connection "+str(source)+ " to "+ str(nodelist[2]))
    r = rpc_create_connection(client, source,nodelist[2],cryptomoney)

    print("*****OK*****")

