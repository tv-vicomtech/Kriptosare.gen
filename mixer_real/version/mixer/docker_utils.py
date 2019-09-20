from conf import *
import docker
import socket
import logging


def get_containers_names(client, prefix=DOCK_CONTAINER_NAME_PREFIX):
    """
    Returns a list of container names.
    :param client: docker client
    :param prefix: string, prefix used in the containers names
    :return: list of strings with container names
    """
    return [container.name for container in client.containers.list("all") if prefix in container.name]


def count_containers(client, prefix=DOCK_CONTAINER_NAME_PREFIX):
    """
    Counts the number of existing containers with a given prefix in their name.
    :param client: docker client
    :param prefix: string, prefix used in the containers names
    :return: number of containers with the specified prefix
    """
    containers = get_containers_names(client)
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


def remove_containers(client, prefix=DOCK_CONTAINER_NAME_PREFIX):
    """
    Removes all containers with a given prefix.
    :param client: docker client
    :param prefix: string, prefix used in the containers names
    :return:
    """
    containers = get_containers_names(client)
    for c in containers:
        if prefix in c:
            remove_container_by_name(client, c)


def get_ip_by_container_name(client, container_name, network_name=DOCK_NETWORK_NAME):
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
    network_name = network_names[0]
    return container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress']


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


def get_ip_by_unknown(client, host):
    """
    Returns the ip of a container given its name or ip
    :param client: docker client
    :param host: container name or ip
    :return: ip address
    """
    if not is_valid_ip(host):
        # If it is not an ip, assume it's a container name:
        host = get_ip_by_container_name(client, host)
    return host

def create_new_service(client,rep, network_name=DOCK_NETWORK_NAME):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    network_names=[network_name,]
    print "*********COUNT CONTAINERS************"
    endpoint_spec_data={'Ports': [{ 'Protocol': 'tcp', 'PublishedPort': 18332, 'TargetPort': 22002 }]}
    print "Services container ..."
    client.services.create(DOCK_IMAGE_NAME,command="bitcoind -datadir=/home/bitcoin/.bitcoin",name="bitcoind",networks=network_names,mode=docker.types.ServiceMode("replicated",rep))
    client.services.create(DOCK_IMAGE_NAME_MIXER,command="./service-up.sh",name="btc_mixer",networks=network_names,mode=docker.types.ServiceMode("replicated",1))

    ########################### START VOLUME SHARED CONTAINER ######################
    port = {'18332/tcp': 22000}
    print "Volume shared container ..." 
    client.containers.run(
        DOCK_IMAGE_NAME_VOLUME,
        "bitcoind -datadir=/home/bitcoin/.bitcoin",
        name=DOCK_CONTAINER_NAME_PREFIX+".volume",
        ports=port,
        detach=True,
        network=network_name
    )

    ########################### START STATOSHI CONTAINER ######################
    port = {'18332/tcp': 22001,
            '80':80,
            '3000':'3000',
            '2003':2003,
            '2004':2004,
            '2023':2023,
            '2024':2024,
            '8125/udp':8125,
            '8126':8126
    }
    print "Statoshi container ..." 
    client.containers.run(
        DOCK_IMAGE_NAME_STATOSHI,
        "/etc/init.d/my_script.sh",
        name=DOCK_CONTAINER_NAME_PREFIX+".statoshi",
        ports=port,
        detach=True,
        network=network_name,
    )



def run_new_node(client, network_name=DOCK_NETWORK_NAME, node_num=None):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    print "*********COUNT CONTAINERS************"
    print count_containers(client)
    containers = client.containers
    if node_num == None:
        c = count_containers(client) + 1
        name = DOCK_CONTAINER_NAME_PREFIX + str(c)
        port = {'18332/tcp': 22001}
    else:
        name = DOCK_CONTAINER_NAME_PREFIX + str(node_num)
        port = {'18332/tcp': 22000 + node_num}

    assert isinstance(containers.run, object)
    if count_containers(client) == 0:
        print "***IN*"
        # print "VOLUMES"
        # volume = client.volumes.create(name='volClient0', driver='local',
        #                                labels={"key": "value"})
        # print(volume)
        # print "*********"
        containers.run(
            DOCK_IMAGE_NAME,
            "bitcoind",
            name=name,
            ports=port,
            detach=True,
            network=network_name,
            #volumes={
            #    '/home/bitcoin/Desktop/BitcoinCourseSoftware/btc_testbed/btc_testbed/data_dir': {
            #        'bind': '/home/bitcoin/.bitcoin/',
            #        'mode': 'rw'}}
        )
    elif count_containers(client) == 6:
        port = {'18332/tcp': 22000 + node_num,
                '80':80,
		        '3000':'3000',
                '2003':2003,
                '2004':2004,
                '2023':2023,
                '2024':2024,
                '8125/udp':8125,
                '8126':8126
            }
        print "***STATOSHI*"
        # print "VOLUMES"
        # volume = client.volumes.create(name='volClient0', driver='local',
        #                                labels={"key": "value"})
        # print(volume)
        # print "*********"
        containers.run(
            DOCK_IMAGE_NAME_STATOSHI,
            #"bitcoind -datadir=/home/statoshi/.bitcoin",
	       "/etc/init.d/my_script.sh",
            name=name,
            ports=port,
            detach=True,
            network=network_name,
        )
    else:
        client.services.create(DOCK_IMAGE_NAME,command="bitcoind",name=name,endpoint_spec=docker.types.EndpointSpec(ports=port))
        #containers.run(DOCK_IMAGE_NAME_2, "bitcoind", name=name, ports=port, detach=True, network=network_name)
    # containers.run("amacneil/bitcoin", "bitcoind", name=name, ports=port, detach=True, network=network_name)


def run_new_nodes(client, n):
    """
    Creates n containers.
    :param client: docker client
    :param n: number of containers to create
    :return:
    """
    for _ in range(n):
        run_new_node(client)


def create_network(client, network_name=DOCK_NETWORK_NAME, subnetwork=DOCK_NETWORK_SUBNET, gw=DOCK_NETWORK_GW):
    """
    Creates a docker network.
    :param client: docker client
    :param network_name: docker network name
    :return:
    """
    try:
        ipam_pool = docker.types.IPAMPool(subnet=subnetwork, gateway=gw)
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        client.networks.create(network_name, driver="overlay", ipam=ipam_config)
    except docker.errors.APIError as err:
        logging.info("    Warning: Network already exists")


def get_container_name_by_ip(client, ip, network_name=DOCK_NETWORK_NAME):
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
