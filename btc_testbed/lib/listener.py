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
	port = 9999
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
						user="vicom",         # your username
						passwd="vicom",  # your password
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
		query = ("SELECT * FROM destination")
		num=json_obj['number']
		cur.execute(query, [args])
		db_list=[]

		for element in cur.fetchall():
			db_list.append(list(element))

		send=db_list[0,int(num)]

		clientsocket.sendall(send)
		print "*****************************************"

