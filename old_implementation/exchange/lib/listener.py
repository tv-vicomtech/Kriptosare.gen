import socket
from rpc_utils import *
import time
from sys import argv
from getopt import getopt
from random import randint
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
		             user="exchange",         # your username
		             passwd="exchange",  # your password
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
	    	#blk = rpc_call_blockcount(client,json_obj['source'],json_obj['fromcurrencies'])
	    	blk = rpc_call_blockcount(client,json_obj['source'],"btc")
	    	confirmations = randint(1,5)
	    	cur = db.cursor()
	    	query = ("insert into exchange (source, destination, fromcurrencies, tocurrencies, amount, confirmations, blk, time) values (%s, %s, %s, %s, %s,%s, %s, %s)")
	    	args = (json_obj['source'],
				json_obj['destination'],
				json_obj['fromcurrencies'], 		        
				json_obj['tocurrencies'], 
				json_obj['amount'],
				confirmations,
				blk,
				json_obj['time'])
	    	cur.execute(query,args)
	    	db.commit() 
	    	print "*****************************************"
	    	print json_obj
