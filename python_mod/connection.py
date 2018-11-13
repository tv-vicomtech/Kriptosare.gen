from rpc_utils import *
from docker_utils import *
import networkx as nx
from btcconf import *
from zchconf import *

import time
from sys import argv
from getopt import getopt
from random import randint


def random_connection_container(client,nodelist,fixname,cryptomoney="btc", connection_number=2):
    connection_number=int(connection_number)
    if(connection_number>=125):
        connection_number=125
    threshold=2*(len(nodelist)-1)

    if(connection_number>threshold):
        connection_number = threshold
        print("Too many connection: reduced to "+str(connection_number))

    if(connection_number >=int(8*len(nodelist)/10)):
        step=len(nodelist)
    else:
        if(len(nodelist)-(int(connection_number*1.5))>0):
            if(connection_number<4):
                step=connection_number+1
            else:
                step= int(connection_number*1.5)
        else:
            step= len(nodelist)

    if(connection_number>16):
        inconn= connection_number-8
        outconn= 8
    else:
        outconn= int(connection_number/2)
        inconn= connection_number-outconn

    connection_address=[]

    x_node_connection(client,fixname,outconn,inconn,nodelist,step,connection_address,connection_number,cryptomoney)
    return


def x_node_connection(client,fixname,outconn,inconn,nodelist,step,connection_address,connection_number,cryptomoney="btc"):
    list_to_remove=[]
    for i in range(1,len(nodelist)+1):
        servername=fixname+str(i)
        #print("************************"+servername)
        #print("***OUT***")
        outcoming_connection(client,servername,i,len(nodelist),step,outconn,inconn,fixname,connection_address,cryptomoney)
    
    list_to_remove=getlistcoinband(connection_address,nodelist,inconn,fixname)

    for i in range(1,len(nodelist)+1):
        servername=fixname+str(i)
        #print("************************"+servername)
        #print("***IN***")
        incoming_connection(client,servername,i,len(nodelist),step,outconn,inconn,fixname,list_to_remove,connection_address,cryptomoney)

def getlistcoinband(connection_address,nodelist,inconn,fixname):
    ll=[]
    for i in range(1,len(nodelist)+1):
        servername=fixname+str(i)
        coninband=countconnection(connection_address,servername,1)
        if(coninband>inconn):
            ll.append(servername)
    return ll

def incoming_connection(client,destination,netsize,endlimit,step,outconn,inconn,fixname,list_to_remove,connection_address,cryptomoney="btc"):
    #conoutband=countconnection(connection_address,destination,0)
    coninband=countconnection(connection_address,destination,1)
    #tot=conoutband+coninband 
    if(coninband<inconn):
        for j in range(coninband,inconn):
            find=True
            if((netsize+step)<endlimit):
                idx=randint(1, (netsize+step))
            else:
                idx=randint(1, endlimit)
            old_idx=idx
            while(find):
                source=fixname+str(idx)
                if(source != destination):
                    if(not findaddress(connection_address,source,destination)):
                        conoutbandsource=countconnection(connection_address,source,0)
                        if(conoutbandsource<outconn):
                            if(cryptomoney=="btc"):
                                r = rpc_create_connection(client, source, destination)
                            elif(cryptomoney=="zch"):
                                r = rpc_create_connection(client, source, destination,cryptomoney,ZCH_RPC_USER,ZCH_RPC_PASSWD,ZCH_RPC_PORT)
                            connection_address.append([source,destination])
                            #print("choose "+ source+","+destination)
                            find=False
                idx=((idx)%(endlimit))+1
                if(old_idx==idx):
                    swap=swapfromlist(client,list_to_remove,connection_address,destination,cryptomoney)
                    find=False

def outcoming_connection(client,source,netsize,endlimit,step,outconn,inconn,fixname,connection_address,cryptomoney="btc"):
    conoutband=countconnection(connection_address,source,0)
    #coninband=countconnection(connection_address,source,1)
    #tot=conoutband+coninband
    old_idx=0
    if(conoutband<outconn):
        for j in range(conoutband,outconn):
            find=True
            if((netsize+step)<endlimit):
                idx=randint(1, (netsize+step))
            else:
                idx=randint(1, endlimit)
            old_idx=idx
            while(find):
                destination=fixname+str(idx)
                if(destination != source):
                    if(not findaddress(connection_address,source,destination)):
                        coninband=countconnection(connection_address,destination,1)
                        if(coninband<inconn):
                            #print source + " "+ destination
                            if(cryptomoney=="btc"):
                                r = rpc_create_connection(client, source, destination)
                            elif(cryptomoney=="zch"):
                                r = rpc_create_connection(client, source, destination,cryptomoney,ZCH_RPC_USER,ZCH_RPC_PASSWD,ZCH_RPC_PORT)
                            connection_address.append([source,destination])
                            #print("choose "+ source+","+destination)
                            find=False
                idx=((idx)%(endlimit))+1
                if(old_idx==idx):
                    inconn=inconn+1

def swapfromlist(client,list_to_remove,connection_address,destination,cryptomoney="btc"):
    idx=-1
    for i in range(0,len(list_to_remove)):
        if(list_to_remove[i]!=destination):
            for j in range(0,len(connection_address)):
                if(connection_address[j][1]==list_to_remove[i] and connection_address[j][0]!=destination):
                    rpc_remove_connection(client, connection_address[j][0], connection_address[j][1],cryptomoney)
                    rpc_create_connection(client, connection_address[j][0], destination,cryptomoney)
                    list_to_remove.remove(list_to_remove[i])
                    connection_address.remove([connection_address[j][0],connection_address[j][1]])
                    connection_address.append([connection_address[j][0],destination])
                    return True
    return False

def countconnection(connection_address,source,idx):
    count = 0
    for i in range(0,len(connection_address)):
        if(connection_address[i][idx]==source):
            count=count+1

    return count

def findaddress(connection_address,source,destination):
    for i in range(0,len(connection_address)):
        if(connection_address[i][0]==source and connection_address[i][1]==destination):
            return True

    return False

def random_connection_element(client,nodelist,nodes_name,fixname,cryptomoney="btc"):
    alreadyadd=[]
    source=nodes_name

    if(len(nodelist)>9):
        connection_number=8
    else:
        connection_number=len(nodelist)

    for i in range(0,connection_number):
        find=True
        idx=randint(1, len(nodelist))
        while(find):
            destination=fixname+str(idx)
            if(source != destination):
                if(destination not in alreadyadd):
                    print source+" "+destination
                    r = rpc_create_connection(client,source ,destination ,cryptomoney)
                    alreadyadd.append(destination)
                    find=False
            idx=(idx)%(len(nodelist))+1


            
