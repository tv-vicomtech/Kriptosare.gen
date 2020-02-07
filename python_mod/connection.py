from rpc_utils import *
from docker_utils import *
import networkx as nx
from btcconf import *
from zchconf import *

import time
from sys import argv
from getopt import getopt
from random import randint

def random_connection_element(client,nodelist,nodes_name,fixname,cryptomoney="btc"):
    alreadyadd=[]
    source=nodes_name
    if(len(nodelist)>9):
        connection_number=8
    else:
        connection_number=len(nodelist)-1

    for i in range(0,connection_number):
        find=True
        idx=randint(1, len(nodelist)+1)
        while(find):
            destination=fixname+str(idx)
            if(source != destination):
                if(destination not in alreadyadd):
                    print(source+" "+destination)
                    r = rpc_create_connection(client,source ,destination ,cryptomoney)
                    time.sleep(1)
                    alreadyadd.append(destination)
                    find=False
            idx=(idx)%(len(nodelist))+1
    return True

def random_connection_element_forexchange(client,nodelist,nodes_name,fixname,cryptomoney="btc"):
    alreadyadd=[]
    destination=nodes_name

    if(len(nodelist)>9):
        connection_number=8
    else:
        connection_number=len(nodelist)
    #print connection_number
    for i in range(0,connection_number):
        find=True
        idx=randint(1, len(nodelist))
        while(find):
            source=fixname+str(idx)
            if(source != destination):
                if(source not in alreadyadd):
                    #print source+" "+destination
                    r = rpc_create_connection(client,source ,destination ,cryptomoney)
                    alreadyadd.append(source)
                    find=False
            idx=(idx)%(len(nodelist))+1

def removeoldexchangeconnection(client,exchange_addr,nodelist_zch,crypto):
    for j in range(0,len(nodelist_zch)):
        r=rpc_remove_connection(client, nodelist_zch[j], exchange_addr,crypto)

def connection_from_graph(client,G,nodelist,fixname,cryptomoney="btc",number_e=0,number_c=0,number_mrk=0,number_p=0,number_mx=0,number_s=0):
    for x in G.edges:
        a = int(x[0])
        if(a+1>number_e+number_c+number_mx+number_mrk+number_p+number_s):
            radix=fixname+str(a+1-(number_e+number_c+number_mx+number_mrk+number_p+number_s))
        elif(a+1>number_e+number_c+number_mx+number_p+number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_MRK+"."+str(a-(number_e+number_c+number_mx+number_p+number_s)+1)
        elif(a+1>number_e+number_c+number_p+number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_MXR+"."+str(a-(number_e+number_c+number_p+number_s)+1)
        elif(a+1>number_e+number_p+number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_CAS+"."+str(a-(number_e+number_p+number_s)+1)
        elif(a+1>number_p+number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_EX+"."+str(a-(number_p+number_s)+1)
        elif(a+1>number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_POOL+"."+str(a-number_s+1)
        else:
            radix=DOCK_CONTAINER_NAME_PREFIX_SER+"."+str(a+1)


        source=radix

        b = int(x[1])
        if(b+1>number_e+number_c+number_mx+number_mrk+number_p+number_s):
            radix=fixname+str(b+1-(number_e+number_c+number_mx+number_mrk+number_p+number_s))
        elif(b+1>number_e+number_c+number_mx+number_p+number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_MRK+"."+str(b-(number_e+number_c+number_mx+number_p+number_s)+1)
        elif(b+1>number_e+number_c+number_p+number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_MXR+"."+str(b-(number_e+number_c+number_p+number_s)+1)
        elif(b+1>number_e+number_p+number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_CAS+"."+str(b-(number_e+number_p+number_s)+1)
        elif(b+1>number_p+number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_EX+"."+str(b-(number_p+number_s)+1)
        elif(b+1>number_s):
            radix=DOCK_CONTAINER_NAME_PREFIX_POOL+"."+str(b-number_s+1)
        else:
            radix=DOCK_CONTAINER_NAME_PREFIX_SER+"."+str(b+1)

        destination=radix

        print("connect "+source +" to "+destination)
        r = rpc_create_connection(client, source,destination,cryptomoney)


            
