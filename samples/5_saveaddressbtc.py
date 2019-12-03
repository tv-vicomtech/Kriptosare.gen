import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *
import pandas as pd
import csv
import logging
from random import randint
import time
from getopt import getopt
from mysocket import *

file_name="/home/titanium/Kriptosare.gen/extdata/labelling.csv"

if __name__ == '__main__':

    client = docker.from_env()

    nodelist=[]
    print("***************************")
    print("Scanning network")
    time.sleep(5)
    nodelist = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")
    nodelist_cas = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_CAS+".")
    nodelist_ex = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_EX+".")
    nodelist_mixer=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_MXR+".")
    nodelist_market=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_MRK+".")
    nodelist_pool=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_POOL+".")
    nodelist_service=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_SER+".")
    
    nodelist.extend(nodelist_cas)
    nodelist.extend(nodelist_ex)
    nodelist.extend(nodelist_mixer)
    nodelist.extend(nodelist_market)
    nodelist.extend(nodelist_pool)
    nodelist.extend(nodelist_service)

    add_info = pd.DataFrame()
    addr_list=[]
    df = pd.DataFrame(columns=['address','amount','user'])

    for source in nodelist:
        inf=rpc_call_alladdress(client,source,cryptotype="btc")
        if(inf):
            sour = []
            test=[]
            amount=[]
            for i in range(0,len(inf)):
                for j in range(0,len(inf[i])):
                   sour.append(source)
                   test.append(inf[i][j][0])
                   addr_list.append(str(inf[i][j][0]))
                   amount.append(inf[i][j][1])
            df=pd.DataFrame({"address":test,'amount':amount,"user":sour})
            add_info=add_info.append(df)
        add_info=add_info.reset_index(drop=True)
    #add_info.to_csv(file_name, sep=',')

    print("New Scanning network")
    #add_info_v2 = pd.DataFrame()
    df = df.iloc[0:0]
    for source in nodelist:
        inf=rpc_call_getaddressbyaccount(client,source,cryptotype="btc")
        if(inf):
            test=[]
            amount=[]
            sour=[]
            for i in range(0,len(inf)):
                if(str(inf[i]) not in addr_list):
                    addr_list.append(str(inf[i]))
                    test.append(inf[i])
                    amount.append(0)
                    sour.append(source)

            df=pd.DataFrame({"address":test,'amount':amount,"user":sour})
            add_info=add_info.append(df)
        add_info=add_info.reset_index(drop=True)
        df = df.iloc[0:0]

    add_info.to_csv(file_name, sep=',')

    print("Store information")
    print("Done")
