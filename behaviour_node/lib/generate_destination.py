import socket
import time
import json
import datetime
import MySQLdb
import numpy as np
from random import randint
from decimal import *
import subprocess
import docker
from rpc_utils import *
import os 

if __name__ == '__main__':
    # name of the data base
	miner_server="localhost"
	db_list=[]
	client = docker.from_env() 
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	user="vicom",         # your username
	passwd="vicom",  # your password
	db="db") 

	while True:
		end=False
		cur = db.cursor()
		query = ("SELECT COUNT(*) FROM destination")
		cur.execute(query)
		
		lenght=0
		for element in cur.fetchall():
			lenght=int(element[0])

		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		ip=s.getsockname()[0]
		s.close()

		add=[]
		end=False
		maxi=15
		while(lenght<=maxi):
			nn=rpc_call(client, ip, "getnewaddress","''")
			add=[nn,ip]
			query = ('INSERT INTO destination (address,IP) values (%s,%s)')
			end = True
			cur.execute(query, add)
			db.commit()
			lenght=lenght+1
			if(lenght%1000==0):
				f = open("info.txt", "a")
				f.write(str(lenght)+" addresses generated\n")
				f.close()
		if(end):
			f = open("info.txt", "a")
			f.write("Generation done..sleep\n")
			f.close()