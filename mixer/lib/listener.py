import socket
import logging
import time
from sys import argv
from getopt import getopt
from random import randint
from rpc_utils import *
import subprocess
import json
import MySQLdb
import os 
import datetime
import docker

from base64 import b64encode

if __name__ == '__main__':
    client = docker.from_env()
    serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 
    host = socket.gethostname()                           
    port = 9999
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="mixer",         # your username
                     passwd="mixer",  # your password
                     db="db")        # name of the data base
    serversocket.bind((host, port))                                  
    serversocket.listen(5)
                                        
    while True:
        clientsocket,addr = serversocket.accept()      
        msg= clientsocket.recv(1024)   
        print("Got a connection from %s" % str(addr))
        print("message: %s" % msg)
        json_obj = json.loads(msg)
        if(json_obj is not None):
            blk=0
            deadline=20
            #blk = rpc_call_blockcount(client,json_obj['source'],json_obj['fromcurrencies'])
            blk = rpc_call_blockcount(client,json_obj['source'],"btc")
            if(int(json_obj['speed'])==1):
                confirmations = randint(2,4)
            elif(int(json_obj['speed'])==2):
                confirmations = randint(4,5)
            else:
                confirmations = -1

            address_in = rpc_call_newaddress(client,json_obj['source'],"btc")

            cur = db.cursor()
            query = ("insert into mixer (source, address_in, destination, amount, confirmations, deadline, blk, time) values (%s, %s, %s, %s, %s,%s, %s, %s)")
            args = (json_obj['source'],
                json_obj['address_in'],
                json_obj['destination'],
                str(json_obj['amount']),
                str(confirmations),
                str(deadline),                 
                str(blk),
                json_obj['time'])
            cur.execute(query,args)
            db.commit() 
            print "*****************************************"
            print json_obj
