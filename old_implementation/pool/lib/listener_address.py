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
	# get local machine name
	host = socket.gethostname()                           
	port = 9998
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
						user="pool",         # your username
						passwd="pool",  # your password
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
			db_list=[]
			cur = db.cursor()
			query = ("SELECT * FROM gen")
			cur.execute(query)
			for element in cur.fetchall():
 				db_list.append(list(element))
 			rr = randint(0,len(db_list)-1)
 			addr = rpc_call(client,host,'getnewaddress')
 			print(addr)
 			print(db_list[rr])
 			print("********************************")
 			isend='{"address":"'+addr+'","idgen":"'+str(db_list[rr][0])+'", "tx":"'+str(db_list[rr][1])+'","amount":"'+db_list[rr][2]+'"}'
 			clientsocket.sendall(isend)

			query=("INSERT INTO transaction (address,tx_rec,amount_rec,tx_sent,amount_sent,balance,uniques,sibling,idgen) values (%s, %s, %s, %s, %s, %s, %s,%s, %s)")            

			args = (addr,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				db_list[rr][0])

			cur.execute(query,args)
			db.commit() 