import socket
import time
import json
import datetime
import MySQLdb
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
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip=s.getsockname()[0]
	s.close()
	end=False
	lenght=0
	add=[]
	maxi=120000
	cur = db.cursor()
	while(lenght<=maxi):
		try:
			nn=rpc_call(client, ip, "getnewaddress","''")
		except:
			nn=0
		if(nn!="" and nn!=False and nn!=None and nn!=0):
			add=[nn,ip]
			query = ('INSERT INTO destination (address,IP) values (%s,%s)')
			end = True
			cur.execute(query, add)
			db.commit()
			f = open("address.csv", "a")
			f.write(str(nn)+","+str(ip)+"\n")
			f.close()
			lenght=lenght+1
		#if(lenght>=maxi):
		#	rpc_call(client,ip,"dumpwallet","'walletdump'")
