#LIB docker for all container/service operations, create, retrive, remove 

from btcconf import *
from zchconf import *
from oconf import *

import docker
import socket
import logging
import time
import logging

def get_containers_names(client, prefix=DOCK_CONTAINER_NAME_PREFIX_BTC):
    """
    Returns a list of container names.
    :param client: docker client
    :param prefix: string, prefix used in the containers names
    :return: list of strings with container names
    """
    return [container.name for container in client.containers.list("all") if prefix in container.name]


def count_containers(client, prefix=DOCK_CONTAINER_NAME_PREFIX_BTC):
    """
    Counts the number of existing containers with a given prefix in their name.
    :param client: docker client
    :param prefix: string, prefix used in the containers names
    :return: number of containers with the specified prefix
    """
    containers = get_containers_names(client,prefix)
    return sum([1 for c in containers if prefix in c])


def remove_container_by_name(client, container_name):
    """
    Removes a container given its name.
    :param client: docker client
    :param container_name: name of the container to remove.
    :return: boolean
    """
    try:
        client.containers.get(container_name).stop()
        return client.containers.get(container_name).remove()
    except docker.errors.NotFound as err:
        return False


def remove_containers(client, prefix=DOCK_CONTAINER_NAME_PREFIX_BTC):
    """
    Removes all containers with a given prefix.
    :param client: docker client
    :param prefix: string, prefix used in the containers names
    :return:
    """
    containers = get_containers_names(client,prefix)
    logging.info(containers)
    for c in containers:
        if prefix in c:
            remove_container_by_name(client, c)


def get_ip_by_container_name(client, container_name, network_name=DOCK_NETWORK_NAME_BTC):
    """
    Returns the ip of a given container (from its name)
    :param client: docker client
    :param container_name: name of the container
    :param network_name: docker network name
    :return: ip address
    """
    try:
        container = client.containers.get(container_name)
    except docker.errors.NotFound as err:
        return False
    network_names = container.attrs['NetworkSettings']['Networks'].keys()
    #assert len(network_names) == 1, "internal error: multiple network names '{}'".format(network_names)
    network_name = list(network_names)[0]

    return container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress']

def get_ip_by_container_name_with_multiple_interface(client, container_name, network_name=DOCK_NETWORK_NAME_BTC):
    """
    Returns the ip of a given container (from its name)
    :param client: docker client
    :param container_name: name of the container
    :param network_name: docker network name
    :return: ip address
    """
    ip=[]
    try:
        container = client.containers.get(container_name)
    except docker.errors.NotFound as err:
        return False
    network_names = container.attrs['NetworkSettings']['Networks'].keys()
    #assert len(network_names) == 1, "internal error: multiple network names '{}'".format(network_names)
    for network_name in network_names:
        ip.append(container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress'])

    return ip


def is_valid_ip(addr):
    """
    Checks if an string is a valid IP
    :param addr: string to check
    :return: boolean, whether the string is a valid IP address.
    """
    try:
        socket.inet_aton(addr)
    except socket.error:
        return False
    return True


def get_ip_by_unknown(client, host,network_name=DOCK_NETWORK_NAME_BTC):
    """
    Returns the ip of a container given its name or ip
    :param client: docker client
    :param host: container name or ip
    :return: ip address
    """
    if not is_valid_ip(host):
        # If it is not an ip, assume it's a container name:
        host = get_ip_by_container_name(client, host,network_name)
    return host

def create_new_service(client,rep, network_name=DOCK_NETWORK_NAME_BTC):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    network_names=[network_name,]
    print("*********COUNT CONTAINERS************")
    #endpoint_spec_data={'Ports': [{ 'Protocol': 'tcp', 'PublishedPort': 18332, 'TargetPort': 22001 }]}
    print("Services container ...")
    client.services.create(DOCK_IMAGE_NAME,command="bitcoind -datadir=/home/bitcoin/.bitcoin",name=DOCK_IMAGE_NAME_BTC,networks=network_names,mode=docker.types.ServiceMode("replicated",rep))

def create_new_mixer_service(client,rep, network_name=DOCK_NETWORK_NAME_BTC):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    network_names=[network_name,]
    print("*********COUNT CONTAINERS************")
    #endpoint_spec_data={'Ports': [{ 'Protocol': 'tcp', 'PublishedPort': 18332, 'TargetPort': 22001 }]}
    print("Services mixer container ...")
    ports={80: 81}
    client.services.create(DOCK_IMAGE_NAME_MIXER,command="./service-up.sh",name=DOCK_IMAGE_NAME_MIXER,networks=network_names,endpoint_spec=docker.types.EndpointSpec("vip",ports),mode=docker.types.ServiceMode("replicated",1))
    

def run_new_nodes(client, n):
    """
    Creates n containers.
    :param client: docker client
    :param n: number of containers to create
    :return:
    """
    for _ in range(n):
        run_new_node(client)

def create_node(client, network_name=DOCK_NETWORK_NAME_BTC, cryptotype="btc", number=1):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """

    containers = client.containers
    if(cryptotype=="btc"):
        for i in range(0,int(number)):
            name = DOCK_IMAGE_NAME_BTC + "." + str(i+1)
            containers.run(
                DOCK_IMAGE_NAME_BTC,
                "bitcoind -datadir=/root/.bitcoin",
                name=name,
                detach=True,
                network=network_name)
    elif (cryptotype=="zch"):
        for i in range(0,int(number)):
            name = DOCK_IMAGE_NAME_ZCH + "." + str(i+1)
            containers.run(
            DOCK_IMAGE_NAME_ZCH,
            "/root/zcash/src/zcashd -datadir=/root/.zcash",
            name=name,
            detach=True,
            network=network_name)

def retrive_network(client, network_name):
    """
    Creates a docker network.
    :param client: docker client
    :param network_name: docker network name
    :return:
    """
    net_list=client.networks.list(filters={'name': network_name})
    if (len(net_list)>0):
	    return True
    return False

def create_network(client, network_name=DOCK_NETWORK_NAME_BTC, subnetwork=DOCK_NETWORK_SUBNET_BTC, gw=DOCK_NETWORK_GW_BTC):
    """
    Creates a docker network.
    :param client: docker client
    :param network_name: docker network name
    :return:
    """
    try:
        net_list=client.networks.list(filters={'name': network_name})
        for net in net_list:
            net.remove()
        
        ipam_pool = docker.types.IPAMPool(subnet=subnetwork, gateway=gw)
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        client.networks.create(network_name, driver="bridge",ipam=ipam_config)
        time.sleep(5)
        client.networks.create(network_name, driver="overlay",ipam=ipam_config)
    except docker.errors.APIError as err:
        logging.info("    Warning: Network already exists")

def get_network_id(client, network_name):
    """
    Creates a docker network.
    :param client: docker client
    :param network_name: docker network name
    :return:
    """
    net_list=client.networks.list(filters={'name': network_name})
    if (net_list):
        return net_list[0].id
    return False

def get_container_name_by_ip(client, ip, network_name=DOCK_NETWORK_NAME_BTC):
    """
    Returns the ip of a given container (from its name)
    :param client: docker client
    :param ip: ip address
    :param network_name: docker network name
    :return: docker container name if found, False otherwise.
    """

    # Sanity check IP formatting
    assert is_valid_ip(ip)

    # Get all the containers connected to the network
    containers = client.networks.get(network_name).containers

    # For each of the containers get the ip by name and check it with the provided ip.
    cont_name = False
    for container in containers:
        if ip == get_ip_by_container_name(client, container.name):
            cont_name = str(container.name)

    return cont_name

def docker_setup(cryptotype="btc", build_image=True, create_docker_network=True, remove_existing=True):
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
        if(cryptotype=="btc"):
            client.images.build(path="btc_testbed", tag=DOCK_IMAGE_NAME_BTC)
        elif(cryptotype=="zch"):
            client.images.build(path="zch_testbed", tag=DOCK_IMAGE_NAME_ZCH)
    if create_docker_network:
        logging.info("  Creating network")
        if(cryptotype=="btc"):
            create_network(client,DOCK_NETWORK_NAME_BTC,DOCK_NETWORK_SUBNET_BTC,DOCK_NETWORK_GW_BTC)
        elif(cryptotype=="zch"):
            create_network(client,DOCK_NETWORK_NAME_ZCH,DOCK_NETWORK_SUBNET_ZCH,DOCK_NETWORK_GW_ZCH)
        
    if remove_existing:
        logging.info("  Removing existing containers")
        if(cryptotype=="btc"):
            remove_containers(client,DOCK_CONTAINER_NAME_PREFIX_BTC)
        elif(cryptotype=="zch"):
            remove_containers(client,DOCK_CONTAINER_NAME_PREFIX_ZCH)

    return client

def check_dock_dashboard(client,cryptotype="btc"):
    V=[]
    stat = blocksci = grph1 = grph2 = grph3 = grph4 = 0
    if(cryptotype=="btc"):
        stat = count_containers(client,DOCK_IMAGE_NAME_STATOSHI)
        blocksci = count_containers(client,DOCK_MACHINE_NAME_BLOCKSCI_BTC)
        grph1 = count_containers(client,DOCK_IMAGE_NAME_CLIENT_BTC)
        grph2 = count_containers(client,DOCK_MACHINE_NAME_DATAFEED_BTC)
        grph3 = count_containers(client,DOCK_IMAGE_NAME_API_BTC)
        grph4 = count_containers(client,DOCK_MACHINE_NAME_DASHBOARD_BTC)
        V.append(stat)
        V.append(blocksci)
        V.append(grph1+grph2+grph3+grph4)
        return V

    elif(cryptotype=="zch"):
        #stat = count_containers(client,DOCK_IMAGE_NAME_STATOSHI)
        #blocksci = count_containers(client,DOCK_IMAGE_NAME_BLOCKSCI_BTC)
        grph1 = count_containers(client,DOCK_IMAGE_NAME_CLIENT_ZCH)
        grph2 = count_containers(client,DOCK_MACHINE_NAME_DATAFEED_ZCH)
        grph3 = count_containers(client,DOCK_IMAGE_NAME_API_ZCH)
        grph4 = count_containers(client,DOCK_MACHINE_NAME_DASHBOARD_ZCH)
        
        V.append(stat)
        V.append(blocksci)
        V.append(grph1+grph2+grph3+grph4)
        return V


def remove_dock_dashboard(client,cryptotype="btc"):
    if(cryptotype=="btc"):
        remove_containers(client,DOCK_IMAGE_NAME_STATOSHI)
        remove_containers(client,DOCK_MACHINE_NAME_BLOCKSCI_BTC)
        remove_containers(client,DOCK_IMAGE_NAME_CLIENT_BTC)
        remove_containers(client,DOCK_MACHINE_NAME_DATAFEED_BTC)
        remove_containers(client,DOCK_IMAGE_NAME_API_BTC)
        remove_containers(client,DOCK_MACHINE_NAME_DASHBOARD_BTC)
    elif(cryptotype=="zch"):
        #remove_containers(client,DOCK_IMAGE_NAME_STATOSHI)
        #remove_containers(client,DOCK_IMAGE_NAME_BLOCKSCI_BTC)
        remove_containers(client,DOCK_IMAGE_NAME_CLIENT_ZCH)
        remove_containers(client,DOCK_MACHINE_NAME_DATAFEED_ZCH)
        remove_containers(client,DOCK_IMAGE_NAME_API_ZCH)
        remove_containers(client,DOCK_MACHINE_NAME_DASHBOARD_ZCH)


def blocksci_setup(build_image, remove_existing, cryptotype="btc"):

    logging.info('Setting up blocksci client')
    client = docker.from_env()
    if build_image:
        logging.info("  Building docker image")
        print(" ********blocksci*****")
        client.images.build(path="../blocksci", tag=DOCK_IMAGE_NAME_BLOCKSCI)
    
    if remove_existing:
        nodes_name=[]
        logging.info("  Removing existing containers")
        if(cryptotype=="btc"):
            namecontainer=client.containers.list(filters={'name': DOCK_MACHINE_NAME_BLOCKSCI_BTC})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
        #elif(cryptotype=="zch"):
        #    namecontainer=client.containers.list(filters={'name': DOCK_MACHINE_NAME_BLOCKSCI_ZCH})
        
        for i in range(0,len(nodes_name)):
            remove_container_by_name(client,nodes_name[i][0].name)
    return client


def generate_dock_blocksci(client, cryptotype="btc"):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    if(cryptotype=="btc"):
        network_name=DOCK_NETWORK_NAME_BTC
        name = DOCK_MACHINE_NAME_BLOCKSCI_BTC
        port = {'8888/tcp':8868}
        CMD="bash /etc/init.d/script.sh"
    elif(cryptotype=="zch"):
        network_name=DOCK_NETWORK_NAME_ZCH
        name = DOCK_MACHINE_NAME_BLOCKSCI_ZCH
        port = {'8888/tcp':8878}
        CMD="bash /etc/init.d/script_zch.sh"

    containers = client.containers

    print("Blocksci")
    containers.run(
        DOCK_IMAGE_NAME_BLOCKSCI,
        CMD,
        name=name,
        detach=True,
        ports=port,
        network=network_name)

def statoshi_setup(build_image, remove_existing, cryptotype="btc"):

    logging.info('Setting up statoshi client')
    client = docker.from_env()
    if build_image:
        logging.info("  Building docker image")
        print(" ********statoshi*****")
        client.images.build(path="statoshi", tag=DOCK_IMAGE_NAME_STATOSHI)
    
    if remove_existing:
        nodes_name=[]
        logging.info("  Removing existing containers")
        if(cryptotype=="btc"):
            namecontainer=client.containers.list(filters={'name': DOCK_IMAGE_NAME_STATOSHI})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
        #elif(cryptotype=="zch"):
            #nodes_name=client.containers.list(filters={'name': DOCK_IMAGE_NAME_STATOSHI})

        for i in range(0,len(nodes_name)):
            remove_container_by_name(client,nodes_name[i][0].name)
    return client


def generate_dock_statoshi(client, cryptotype="btc"):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    if(cryptotype=="btc"):
        network_name=DOCK_NETWORK_NAME_BTC
        name = DOCK_IMAGE_NAME_STATOSHI
        port = {'3000/tcp':3010}
        CMD="/etc/init.d/my_script.sh"

    #elif(cryptotype=="zch"):
    #    network_name=DOCK_NETWORK_NAME_ZCH
    #    name = DOCK_IMAGE_NAME_STATOSHI
    #    port = {'3000/tcp':3020}
    #    CMD="/etc/init.d/my_script.sh"

    containers = client.containers

    print("Statoshi")
    containers.run(
        name,
        CMD,
        name=name,
        detach=True,
        ports=port,
        network=network_name)

def grph_setup(build_image, remove_existing, cryptotype="btc"):

    logging.info('Setting up graphsense client')
    client = docker.from_env()
    if build_image:
        logging.info("  Building docker image")
        #print(" ********client*****")
        #client.images.build(path="graphsense/bitcoin-client", tag=DOCK_IMAGE_NAME_CLIENT)
        if(cryptotype=="btc"):
            print(" ********api*****")
            client.images.build(path="graphsense/api/btc", tag=DOCK_IMAGE_NAME_API_BTC)
        elif(cryptotype=="zch"):
            print(" ********api*****")
            client.images.build(path="graphsense/api/zch", tag=DOCK_IMAGE_NAME_API_ZCH)

        print(" ********datafeed*****")
        client.images.build(path="graphsense/data-feed", tag=DOCK_IMAGE_NAME_DATAFEED)

        print(" ********dashboard*****")
        client.images.build(path="graphsense/graphsense-dashboard", tag=DOCK_IMAGE_NAME_DASHBOARD)
    
    if remove_existing:
        nodes_name=[]
        namecontainer=[]
        logging.info("  Removing existing containers")
        if(cryptotype=="btc"):
            namecontainer=client.containers.list(filters={'name': DOCK_IMAGE_NAME_CLIENT_BTC})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
            namecontainer=client.containers.list(filters={'name': DOCK_MACHINE_NAME_DATAFEED_BTC})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
            namecontainer=client.containers.list(filters={'name': DOCK_IMAGE_NAME_API_BTC})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
            namecontainer=client.containers.list(filters={'name': DOCK_MACHINE_NAME_DASHBOARD_BTC})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
        elif(cryptotype=="zch"):
            namecontainer=client.containers.list(filters={'name': DOCK_IMAGE_NAME_CLIENT_ZCH})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
            namecontainer=client.containers.list(filters={'name': DOCK_MACHINE_NAME_DATAFEED_ZCH})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
            namecontainer=client.containers.list(filters={'name': DOCK_IMAGE_NAME_API_ZCH})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
            namecontainer=client.containers.list(filters={'name': DOCK_MACHINE_NAME_DASHBOARD_ZCH})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
        if(len(namecontainer)>0):
            nodes_name.append(namecontainer)
        for i in range(0,len(nodes_name)):
            remove_container_by_name(client,nodes_name[i][0].name)
    return client

def generate_dock_grph(client, cryptotype="btc"):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    containers = client.containers

    if(cryptotype=="btc"):
        name = DOCK_IMAGE_NAME_CLIENT_BTC
        mach=DOCK_IMAGE_NAME_BTC
        CMD = "bitcoind -rest -datadir=/root/.bitcoin"
        network_name=DOCK_NETWORK_NAME_BTC
    elif(cryptotype=="zch"):
        name = DOCK_IMAGE_NAME_CLIENT_ZCH
        mach=DOCK_IMAGE_NAME_ZCH
        CMD = "/root/zcash/src/zcashd -datadir=/root/.zcash"
        network_name=DOCK_NETWORK_NAME_ZCH

    print("Client")
    containers.run(
        mach,
        CMD,
        name=name,
        detach=True,
        network=network_name)


    if(cryptotype=="btc"):
        name = DOCK_MACHINE_NAME_DATAFEED_BTC
        CMD = "/etc/init.d/script.sh"
        network_name=DOCK_NETWORK_NAME_BTC
    elif(cryptotype=="zch"):
        name = DOCK_MACHINE_NAME_DATAFEED_ZCH
        CMD = "/etc/init.d/script20.sh"
        network_name=DOCK_NETWORK_NAME_ZCH

    print("DATAFEED")
    containers.run(
        DOCK_IMAGE_NAME_DATAFEED,
        CMD,
        name=name,
        detach=True,
        network=network_name)

    time.sleep(40)

    if(cryptotype=="btc"):
        name = DOCK_IMAGE_NAME_API_BTC
        CMD = "/etc/init.d/script.sh"
        network_name=DOCK_NETWORK_NAME_BTC
    elif(cryptotype=="zch"):
        name = DOCK_IMAGE_NAME_API_ZCH
        CMD = "/etc/init.d/script.sh"
        network_name=DOCK_NETWORK_NAME_ZCH
    
    print("API")
    containers.run(
        name,
        CMD,
        name=name,
        detach=True,
        network=network_name)

    if(cryptotype=="btc"):
        name = DOCK_MACHINE_NAME_DASHBOARD_BTC
        CMD = "/etc/init.d/script.sh"
        network_name=DOCK_NETWORK_NAME_BTC
        port = {'8000/tcp':8000}
    elif(cryptotype=="zch"):
        name = DOCK_MACHINE_NAME_DASHBOARD_ZCH
        CMD = "/etc/init.d/script_zch.sh"
        network_name=DOCK_NETWORK_NAME_ZCH
        port = {'8000/tcp':8010}

    print("Dashboard")
    containers.run(
        DOCK_IMAGE_NAME_DASHBOARD,
        CMD,
        name=name,
        ports=port,
        detach=True,
        network=network_name)
    
def create_behvnode(client, number=1, name_behv=DOCK_IMAGE_NAME_EX,prefix_behv=DOCK_CONTAINER_NAME_PREFIX_EX):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    containers = client.containers
    namecontainer=client.containers.list(filters={'name': name_behv})
    num=len(namecontainer)
    for i in range(0,int(number)):
        name = prefix_behv + "." + str(i+1+num)
        containers.run(
            name_behv,
            "bash /etc/init.d/script.sh",
            name=name,
            detach=True,
            network=DOCK_NETWORK_NAME_BTC)
        time.sleep(5)
        #if(retrive_network(client,DOCK_NETWORK_NAME_ZCH)):
        #    id_net=get_network_id(client,DOCK_NETWORK_NAME_ZCH)
        #    net=client.networks.get(id_net)
        #    net.connect(name)


def getalladdress(client,nodelist):
    dest_add=[]
    for source in nodelist:
        dest_add.append(rpc_call(client, source, 'getnewaddress'))
    return dest_add

def collector_setup(build_image, remove_existing, cryptotype="btc"):

    logging.info('Setting up data collector client')
    client = docker.from_env()
    if build_image:
        logging.info("  Building docker image")
        #print(" ********client*****")
        #client.images.build(path="graphsense/bitcoin-client", tag=DOCK_IMAGE_NAME_CLIENT)
        print(" ********datafeed*****")
        client.images.build(path="../graphsense/data-feed", tag=DOCK_IMAGE_NAME_DATAFEED)

    
    if remove_existing:
        nodes_name=[]
        namecontainer=[]
        logging.info("  Removing existing containers")
        if(cryptotype=="btc"):
            namecontainer=client.containers.list(filters={'name': DOCK_IMAGE_NAME_CLIENT_BTC})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
            namecontainer=client.containers.list(filters={'name': DOCK_MACHINE_NAME_DATAFEED_BTC})
            if(len(namecontainer)>0):
                nodes_name.append(namecontainer)
        if(len(namecontainer)>0):
            nodes_name.append(namecontainer)
        for i in range(0,len(nodes_name)):
            remove_container_by_name(client,nodes_name[i][0].name)
    return client

def generate_collector(client, cryptotype="btc"):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    containers = client.containers


    name = DOCK_IMAGE_NAME_CLIENT_BTC
    mach=DOCK_IMAGE_NAME_BTC
    CMD = "bitcoind -rest -datadir=/root/.bitcoin"
    network_name=DOCK_NETWORK_NAME_BTC

    print("Client")
    containers.run(
        mach,
        CMD,
        name=name,
        detach=True,
        network=network_name)


    name = DOCK_MACHINE_NAME_DATAFEED_BTC
    CMD = "/etc/init.d/script.sh"
    network_name=DOCK_NETWORK_NAME_BTC
    port = {'9042':9042}

    print("DATAFEED")
    containers.run(
        DOCK_IMAGE_NAME_DATAFEED,
        CMD,
        name=name,
        detach=True,
        ports=port,
        network=network_name)
