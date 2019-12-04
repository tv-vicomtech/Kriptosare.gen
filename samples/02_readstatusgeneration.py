import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *
import logging
import time
import MySQLdb

file_name="/info.txt"

if __name__ == '__main__':

    client = docker.from_env()

    nodelist=[]
    print("***************************")
    nodelist= get_containers_names(client, "btc.")
    nodelist_pool= get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_POOL+".")
    nodelist_ex = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_EX+".")
    nodelist_gam = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_CAS+".")
    nodelist_mrk = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_MRK+".")
    nodelist_mxr = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_MXR+".")
    nodelist_ser = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_SER+".")

    nodelist_behavioural=nodelist_pool+nodelist_ex+nodelist_gam+nodelist_mrk+nodelist_mxr+nodelist_ser
    nodelist=nodelist+nodelist_behavioural

    for source in nodelist:
        source_ip=get_ip_by_container_name(client, source)
        mydb = MySQLdb.connect(host=source_ip,
        user='vicom',
        passwd='vicom',
        db='db')
        cursor = mydb.cursor()
        cursor.execute('SELECT COUNT(*) from destination')
        lenght=0
        for element in cursor.fetchall():
            lenght=int(element[0])
        print(str(source)+": "+str(lenght)+" addresses")
    print("Done")
