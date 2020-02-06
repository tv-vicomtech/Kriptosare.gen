import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *
import os
import logging
from random import randint
import time
from getopt import getopt
from mysocket import *
import csv
import MySQLdb
import subprocess

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
        client.images.build(path="../behaviour_node", tag=DOCK_IMAGE_NAME_BEH)
 

    if create_docker_network:
        create_network(client)
    if remove_existing:
        remove_containers(client)
    return client



def import_configuration(client, nodel):
    containers = client.containers.list()
    hh=41
    for i in range(0,len(nodel)):
        source=get_ip_by_container_name(client, nodel[i])
        try:
            #mydb = MySQLdb.connect(host=source,
            #user='vicom',
            #passwd='vicom',
            #db='db')
            #cursor = mydb.cursor()
            #with open('/home/titanium/Kriptosare.gen/backupwallet/address'+str(i)+'.csv', mode='r') as csv_file:
            #    csv_reader = csv.reader(csv_file, delimiter=',')
            #    for row in csv_reader:
            #        nn=[row[0],source]
            #        cursor.execute('INSERT INTO destination(address,IP) VALUES("%s", "%s")', nn)
            #        mydb.commit()
            #cursor.close()
            strn='docker cp /home/titanium/Kriptosare.gen/backupwallet/walletdump'+str(hh)+' '+nodelist[i]+':/root/.bitcoin/walletdump'+str(hh)
            print(strn)
            subprocess_cmd(strn)
            strn='docker exec -d '+str(nodelist[i])+' bitcoin-cli importwallet "/root/.bitcoin/walletdump'+str(hh)+'"'
            print(strn)
            subprocess_cmd(strn)
            with open("/home/titanium/Kriptosare.gen/backupwallet/relation.csv", 'a') as f:
                f.write(str(hh)+","+nodelist[i]+"\r\n")
            hh=hh+1
        except:
            print("No DB...error")

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()

def starting_generator(nodelist):
    for uuid in nodelist:
        strn="docker exec -d "+str(uuid)+" nohup python /root/lib/generate_destination.py;"
        subprocess_cmd(strn)
        print(strn+"...started")


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
    G= nx.read_graphml('../graphml/model/model0_10.graphml')

    nodelist=[]
    print("***************************")
    print("*********CREATE CONTAINERS************")
    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."

    number_pool = 0
    number_ex = 0
    number_cas = 0
    number_mrk = 0
    number_mxr = 0
    number_ser = 0
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
    print("***************************")
    print("Starting services")
    print("Wait 120 seconds...")
    tool_bar(300)
    print("***************************")
    print("import configutation")
    print("Wait 360 seconds...")
    nodelist = get_containers_names(client, fixname)
   
    tool_bar(360)
    import_configuration(client, nodelist)
    print("***************************")
    print("Start connection")
    connection_from_graph(client,G,nodelist,fixname,"btc",number_ex,number_cas,number_mrk,number_pool,number_mxr,number_ser)
    print("***************************")
    print("Starting generator")
    print("Wait 60 seconds...")
    tool_bar(60)
    starting_generator(nodelist)
    print("***************************")
    print("END!")
    