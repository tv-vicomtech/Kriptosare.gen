import socket
import logging
import time
from sys import argv
from getopt import getopt
from random import randint
import subprocess
import json
import MySQLdb
import os 
import datetime
from base64 import b64encode

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

    logging.info('Setting up docker client')
    client = docker.from_env()
    
    return client

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9999

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="vicomtech",         # your username
                     passwd="vicomtech",  # your password
                     db="db")        # name of the data base
# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)   
                                        
while True:
    clientsocket,addr = serversocket.accept()      
    msg= clientsocket.recv(1024)   
    print("Got a connection from %s" % str(addr))
    print("message: %s" % msg)
    json_obj = json.loads(msg)

    cur = db.cursor()
    query = ("SELECT * FROM accounts WHERE input_address =%s")
    cur.execute(query,[json_obj['from']])
    if (cur.rowcount<1):
        p=subprocess.Popen('bitcoin-cli getnewaddress ""',stdout=subprocess.PIPE,shell=True)
        (output,err) = p.communicate()
        output = output.replace(" ","").rstrip()
        print "*** Generated new address: "+output
        rand_string = os.urandom(32)
        token = rand_string.encode('hex')
        dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = ("insert into accounts (input_address, required_confirmations, secret_mixing_key,created_datetime) values (%s,%s,%s,%s)")
        confirmed=2;
        if (json_obj['velocity']=="1"):
            confirmed=randint(2, 5)
        else:
            confirmed=randint(6, 24)
        cur.execute(query,[output,str(confirmed),token,dt])
        query = ("SELECT account_id FROM accounts WHERE input_address =%s")
        cur.execute(query,[output])
        if (cur.rowcount<1):
            print "Internal Error"
            data = '{"address":"-2","key":"-2","confirmed":"-2"}'
            clientsocket.send(data)

        else:
            rows = cur.fetchall()
            acc_id=rows[0]
            query = ("insert into output_addresses (account_id, output_address) values (%s, %s)")
            cur.execute(query,[acc_id,json_obj['to']])
            db.commit() 
            print "*****************************************"
            data = '{"address":"'+output+'","key":"'+token+'","confirmed":"'+str(confirmed)+'"}'
            clientsocket.send(data)
    else:
        print "Address already involved in operation"
        data = '{"address":"-1","key":"-1","confirmed":"-1"}'
        clientsocket.send(data)
    clientsocket.close()
