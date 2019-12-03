import sys

sys.path.insert(0, '../python_mod')

from rpc_utils import *
from docker_utils import *
from oconf import *
from sendlib import *
from connection import *

import logging
from random import randint
import time, datetime
from getopt import getopt


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
    client = docker.from_env()


    ####################################################################################################
    ### CASINO #########################################################################################
    ####################################################################################################

    #fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
    #nodelist=get_containers_names(client, fixname)

    #fixname_cas=DOCK_CONTAINER_NAME_PREFIX_CAS+"."
    #nodelist_cas=get_containers_names(client, fixname_cas)

    #send_to_casino(client,nodelist[0],"btc","1",datetime.datetime.now(),nodelist_cas[0])

    ####################################################################################################
    ### EXCHANGE #######################################################################################
    ####################################################################################################


    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
    nodelist=get_containers_names(client, fixname)

    fixname_zch=DOCK_CONTAINER_NAME_PREFIX_ZCH+"."
    nodelist_zch=get_containers_names(client, fixname_zch)

    fixname_ex=DOCK_CONTAINER_NAME_PREFIX_EX+"."
    nodelist_ex=get_containers_names(client, fixname_ex)

    mynewaddresszch=rpc_call_newaddress(client,nodelist_zch[0],"zch")
    mynewaddressbtc=rpc_call_newaddress(client,nodelist[3],"btc")
    send_to_exchange(client,nodelist[0],mynewaddresszch,"btc","zch","1",datetime.datetime.now(),nodelist_ex[0])
    send_to_exchange(client,nodelist_zch[3],mynewaddressbtc,"zch","btc","1",datetime.datetime.now(),nodelist_ex[0])

    print "Done"

