import socket
import logging
import time
from sys import argv
from getopt import getopt
from random import randint
import subprocess
import json
#import MySQLdb
import os 
import datetime
import docker
from base64 import b64encode


if __name__ == '__main__':
	client = docker.from_env()
	serversocket = socket.socket(
			socket.AF_INET, socket.SOCK_STREAM) 
	# get local machine name
	host = socket.gethostname()                           
	port = 9999
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		             user="mixer",         # your username
		             passwd="mixer",  # your password
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
	    if(json_obj is not None):
		blk = rpc_call_blockcount(client,json_obj['source'],json_obj['currencies']):
	    	confirmations = randint(1,5)
		cur = db.cursor()
		query = ("insert into mixer (source, destination, currencies, amount, confirmations, blk, time) values (%s, %s, %s, %s, %d, %d, %s)")
		args = (json_obj['source'],
		        json_obj['destination'], 		        
			json_obj['currencies'], 
			json_obj['amount'],
			confirmations,
			blk,
		        json_obj['time'])
	    	cur.execute(query, args)
		db.commit() 
		print "*****************************************"
		print json_obj