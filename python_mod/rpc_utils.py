#RPC LIB for all operation trought the bitcoin API
from btcconf import *
from zchconf import *

from docker_utils import *
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


def rpc_getinfo(client, rpc_server, rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Tests a rpc connection to a given container.
    :param client: docker client
    :param rpc_server: container IP (with bitcoind running)
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: boolean, whether the connection was successful
    """
    try:
        rpc_server = get_ip_by_unknown(client, rpc_server)
        # Test connection by sendinf a getinfo command
        rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
        get_info = rpc_connection.getinfo()
        return get_info
    except JSONRPCException as err:
        return False


def rpc_test_connection(client, rpc_server, rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Tests a rpc connection to a given container.
    :param client: docker client
    :param rpc_server: container IP (with bitcoind running)
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: boolean, whether the connection was successful
    """
    try:
        get_info = rpc_getinfo(client, rpc_server, rpc_user=rpc_user, rpc_password=rpc_password, rpc_port=rpc_port)
        print(get_info)
        return True
    except JSONRPCException as err:
        return False


def rpc_getpeerinfo(client, rpc_server, rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Sends a rpc: getpeerinfo call to a given container.
    :param client: docker client
    :param rpc_server: container IP (with bitcoind running)
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: result of the rpc call or False
    """
    try:
        rpc_server = get_ip_by_unknown(client, rpc_server)
        rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
        peerinfo = rpc_connection.getpeerinfo()
        return peerinfo
    except JSONRPCException as err:
        return False


def rpcp_get_peer_ips(client, rpc_server, rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Returns a list of ips addresses of the peers connected to the node, together with a boolean indicating
    in the connection is inboud.
    :param client: docker client
    :param rpc_server: container IP (with bitcoind running)
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: list of tuples, each tuple has (IP, inbound?)
    """
    peerinfo = rpc_getpeerinfo(client, rpc_server, rpc_user=rpc_user, rpc_password=rpc_password, rpc_port=rpc_port)

    peer_ips = []

    for peer in peerinfo:
        if peer['inbound']:
            peer_ip, peer_port = str.split(str(peer['addr']), ':')
            peer_ips.append((peer_ip, peer["inbound"]))
        else:
            peer_ips.append((peer["addr"], peer["inbound"]))

    return peer_ips


def rpc_create_connection(client, source, dest,crypto="btc",
                          rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Creates a connection between two bitcoind nodes (from source to dest).
    Both ends must be running a bitcoind instance.

    :param client: docker client
    :param source: container IP (with bitcoind running)
    :param dest: container IP (with bitcoind running)
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: boolean, whether the connection was successful
    """
    try:
        if(crypto=="btc"):
            rpc_server = get_ip_by_unknown(client, source)
            dest = get_ip_by_unknown(client, dest)
            rpc_port=BTC_RPC_PORT
            rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
            r=rpc_connection.addnode(dest, "add")
            #print rpc_user+" "+rpc_password+" "+rpc_server+ " "+str(rpc_port)+ " "+dest

        elif(crypto=="zch"):
            rpc_server_list = get_ip_by_container_name_with_multiple_interface(client, source,DOCK_NETWORK_NAME_ZCH)
            dest_list = get_ip_by_container_name_with_multiple_interface(client, dest,DOCK_NETWORK_NAME_ZCH)
            rpc_port=ZCH_RPC_PORT

            if(len(rpc_server_list)>1):
                rpc_server=rpc_server_list[1]
            else:
                rpc_server=rpc_server_list[0]

            if(len(dest_list)>1):
                dest=dest_list[1]
            else:
                dest=dest_list[0]

            rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
            r=rpc_connection.addnode(dest, "add")
            #rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
            #r=rpc_connection.addnode(dest, "onetry")
            #print rpc_user+" "+rpc_password+" "+rpc_server+ " "+str(rpc_port)+ " "+dest

        return True
    except JSONRPCException as err:
        print(err)
        return False

def rpc_create_connection_onetry(client, source, dest,crypto="btc",
                          rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Creates a connection between two bitcoind nodes (from source to dest).
    Both ends must be running a bitcoind instance.

    :param client: docker client
    :param source: container IP (with bitcoind running)
    :param dest: container IP (with bitcoind running)
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: boolean, whether the connection was successful
    """
    try:
        if(crypto=="btc"):
            rpc_server = get_ip_by_unknown(client, source)
            dest = get_ip_by_unknown(client, dest)
            rpc_port=BTC_RPC_PORT
            rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
            r=rpc_connection.addnode(dest, "add")
            #print rpc_user+" "+rpc_password+" "+rpc_server+ " "+str(rpc_port)+ " "+dest

        elif(crypto=="zch"):
            rpc_server_list = get_ip_by_container_name_with_multiple_interface(client, source,DOCK_NETWORK_NAME_ZCH)
            dest_list = get_ip_by_container_name_with_multiple_interface(client, dest,DOCK_NETWORK_NAME_ZCH)
            rpc_port=ZCH_RPC_PORT

            if(len(rpc_server_list)>1):
                rpc_server=rpc_server_list[1]
            else:
                rpc_server=rpc_server_list[0]

            if(len(dest_list)>1):
                dest=dest_list[1]
            else:
                dest=dest_list[0]

            rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
            r=rpc_connection.addnode(dest, "add")
            #rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
            r=rpc_connection.addnode(dest, "onetry")
            #print rpc_user+" "+rpc_password+" "+rpc_server+ " "+str(rpc_port)+ " "+dest

        return True
    except JSONRPCException as err:
        print(err)
        return False


def rpc_remove_connection(client, source, dest,crypto="btc",
                          rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Creates a connection between two bitcoind nodes (from source to dest).
    Both ends must be running a bitcoind instance.

    :param client: docker client
    :param source: container IP (with bitcoind running)
    :param dest: container IP (with bitcoind running)
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: boolean, whether the connection was successful
    """
    try:
        if(crypto=="btc"):
            rpc_server = get_ip_by_unknown(client, source)
            dest = get_ip_by_unknown(client, dest)
            rpc_port=BTC_RPC_PORT
        else:
            rpc_server_list = get_ip_by_container_name_with_multiple_interface(client, source,DOCK_NETWORK_NAME_ZCH)
            dest_list = get_ip_by_container_name_with_multiple_interface(client, dest,DOCK_NETWORK_NAME_ZCH)
            rpc_port=ZCH_RPC_PORT

            if(len(rpc_server_list)>1):
                rpc_server=rpc_server_list[1]
            else:
                rpc_server=rpc_server_list[0]

            if(len(dest_list)>1):
                dest=dest_list[1]
            else:
                dest=dest_list[0]
        rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
        r=rpc_connection.addnode(dest, "remove")
        return True
    except JSONRPCException as err:
        #print(err)
        return False

def rpc_call(client, rpc_server, call, arguments=None,
                     rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Sends a rpc call to a given container.

    :param client: docker client
    :param rpc_server: container IP (with bitcoind running)
    :param call: rpc call to send
    :param arguments: arguments to the rpc call
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: result of the rpc call or False
    """
    try:
        rpc_server = get_ip_by_unknown(client, rpc_server)
        rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
        args = "(" + arguments + ")" if arguments else "()"
        r = eval("rpc_connection." + call + args)
        return r
    except JSONRPCException as err:
        print(err)
        return False


def rpc_call_to_all(client, call, prefix=DOCK_CONTAINER_NAME_PREFIX_BTC, arguments=None,
                    rpc_user=BTC_RPC_USER, rpc_password=BTC_RPC_PASSWD, rpc_port=BTC_RPC_PORT):
    """
    Sends a rpc call to all containers with a given prefix in their name.

    :param client: docker client
    :param call: rpc call to send
    :param prefix: string, prefix to find in containers' names
    :param arguments: arguments to the rpc call
    :param rpc_user: bitcoind rpc user
    :param rpc_password: bitcoind rpc password
    :param rpc_port: bitcoind rpc port
    :return: a list with the results of the rpc calls or False
    """
    try:
        containers = get_containers_names(client, prefix)
        r = []
        for c in containers:
            rpc_server = get_ip_by_unknown(client, c)
            rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_server, rpc_port))
            args = "(" + arguments + ")" if arguments else "()"
            r.append(eval("rpc_connection." + call + args))
        return r
    except JSONRPCException as err:
        return False


def rpcp_get_network_topology(client):
    """
    Gets the network topology as a dict.
    :param client: docker client
    :return: Network topology
    """

    # Initialize topology dictionary and get container names.
    net_topology = {}
    containers = map(str, get_containers_names(client))

    for container in containers:
        net_topology[container] = []
        # For each container get the list of peer ips.
        for ip, inbound in rpcp_get_peer_ips(client, container):
            peer_name = get_container_name_by_ip(client, ip)
            # Add the id as a peer specifying whether the connection is inbound or not
            net_topology[container].append((peer_name, inbound))

    return net_topology

def rpc_call_blockcount(client,source,cryptotype="btc"):
    n=0
    if(cryptotype=="btc"):
        n=rpc_call(client, source, "getblockcount","")
    elif(cryptotype=="zch"):
        n=rpc_call(client, source, "getblockcount","",ZCH_RPC_USER, ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    return str(n)

def rpc_call_blockhash(client,source,num,cryptotype="btc"):
    if(cryptotype=="btc"):
        hash_last=rpc_call(client, source, "getblockhash",num)
    elif(cryptotype=="zch"):
        hash_last=rpc_call(client, source, "getblockhash",num,ZCH_RPC_USER, ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    return hash_last

def rpc_call_blockinfo(client,source,hash_last,cryptotype="btc"):
    if(cryptotype=="btc"):
        tx_last=rpc_call(client, source, "getblock",'"'+hash_last+'"')
    elif(cryptotype=="zch"):
        tx_last=rpc_call(client, source, "getblock",'"'+hash_last+'"',ZCH_RPC_USER, ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    return tx_last

def rpc_call_walletinfo(client,source,cryptotype="btc"):
    if(cryptotype=="btc"):
        walletinfo=rpc_call(client, source, "getwalletinfo","")
    elif(cryptotype=="zch"):
        walletinfo=rpc_call(client, source, "getwalletinfo","",ZCH_RPC_USER, ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    return walletinfo

def rpc_call_balance(client,source,cryptotype="btc"):
    balance=0
    if(cryptotype=="btc"):
        balance=rpc_call(client, source, "getbalance","")
    elif(cryptotype=="zch"):
        balance=rpc_call(client, source, "getbalance","",ZCH_RPC_USER, ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    return balance

def rpc_call_accountaddress(client,source,cryptotype="btc"):
    if(cryptotype=="btc"):
        address_account=rpc_call(client, source, "getaccountaddress","''")
    elif(cryptotype=="zch"):
        address_account=rpc_call(client, source, "getaccountaddress","''",ZCH_RPC_USER, ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    return address_account

def rpc_call_newaddress(client,source,cryptotype="btc"):
    if(cryptotype=="btc"):
        new_address=rpc_call(client, source, "getnewaddress","''")
    elif(cryptotype=="zch"):
        new_address=rpc_call(client, source, "getnewaddress","''",ZCH_RPC_USER, ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    return new_address

def rpc_call_listunspent(client,source,cryptotype="btc"):
    listunspent=""
    if(cryptotype=="btc"):
        listunspent=rpc_call(client, source, "listunspent","")
    elif(cryptotype=="zch"):
        listunspent=rpc_call(client, source, "listunspent","",ZCH_RPC_USER, ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    return listunspent

def rpc_call_sendmondey(client,source,destination,amount,cryptotype="btc"):
    if(cryptotype=="zch"):
        rpc_call(client, source, "sendtoaddress", "'"+destination+"','"+amount+"'",ZCH_RPC_USER,ZCH_RPC_PASSWD,ZCH_RPC_PORT)
    elif(cryptotype=="btc"):
        rpc_call(client, source, "sendtoaddress", "'"+destination+"','"+amount+"'",BTC_RPC_USER,BTC_RPC_PASSWD,BTC_RPC_PORT)

def rpc_call_createrawtransaction(client,origen,transtot,cryptotype="btc"):
    if(cryptotype=="btc"):
        rawtx = rpc_call(client, origen, 'createrawtransaction', transtot)
    elif(cryptotype=="zch"):
        rawtx = rpc_call(client, origen, 'createrawtransaction', transtot,ZCH_RPC_USER, ZCH_RPC_PASSWD, ZCH_RPC_PORT)
    return rawtx

def rpc_call_signrawtransaction(client,origen,params,cryptotype="btc"):
    if(cryptotype=="btc"):
        signrawtx = rpc_call(client, origen, 'signrawtransaction', params)
    elif(cryptotype=="zch"):
        signrawtx = rpc_call(client, origen, 'signrawtransaction', params,ZCH_RPC_USER, ZCH_RPC_PASSWD, ZCH_RPC_PORT)
    return signrawtx

def rpc_call_sendrawtransaction(client,origen,rawtrans,cryptotype="btc"):
    if(cryptotype=="btc"):
        rtxid = rpc_call(client, origen, 'sendrawtransaction', rawtrans)
    elif(cryptotype=="zch"):
        rtxid = rpc_call(client, origen, 'sendrawtransaction', rawtrans, ZCH_RPC_USER, ZCH_RPC_PASSWD, ZCH_RPC_PORT)
    return rtxid

def rpc_call_generate(client,origen,number="1",cryptotype="btc"):
    if(cryptotype=="btc"):
        gen = rpc_call(client, origen, 'generate', str(number))
    elif(cryptotype=="zch"):
        gen = rpc_call(client, origen, 'generate', str(number), ZCH_RPC_USER, ZCH_RPC_PASSWD, ZCH_RPC_PORT)
    return gen

def rpc_call_dumpprivkey(client,origen,txaddr,cryptotype="btc"):
    if(cryptotype=="btc"):
        dpk=rpc_call(client, origen, 'dumpprivkey', '"' + str(txaddr) +'"')
    elif(cryptotype=="zch"):
        dpk = rpc_call(client, origen, 'dumpprivkey', '"' + str(txaddr) +'"', ZCH_RPC_USER, ZCH_RPC_PASSWD, ZCH_RPC_PORT)
    return dpk
