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
		query = ("SELECT * FROM received_tx where destination=%s")
		args=json_obj['destination']
		cur.execute(query, [args])
		db_list=[]

		for element in cur.fetchall():
			db_list.append(list(element))

		if(len(db_list)>0):
			confirmations=db_list[0][5]
		else:
			confirmations = randint(4,8)

		if(json_obj is not None):
			blk = rpc_call_blockcount(client,json_obj['source'],json_obj['currencies'])
			query = ("insert into received_tx (source, destination, currencies, amount, confirmations, blk, time) values (%s, %s, %s, %s, %s, %s, %s)")
			args = (json_obj['source'],
					json_obj['destination'],
					json_obj['currencies'], 		        
					json_obj['amount'],
					confirmations,
					int(blk),
					json_obj['time'])
			cur.execute(query,args)
			db.commit() 

			############################################################################################
			db_tx_rcv=0
			db_tx_sent=0
			db_balance=0
			db_amount_rec=0
			db_amount_sent=0
			db_sibling=0
			idgen=0
			comp=0

			cur = db.cursor()

			query = ("SELECT * FROM transaction where address=%s")
			#print db_list
			dd=str(json_obj['destination'])
			cur.execute(query,[dd])
			for element in cur.fetchall():
				db_tx_rcv=element[2]
				db_tx_sent=element[4]
				db_balance=element[6]
				db_amount_rec=element[3]
				db_amount_sent=element[5]
				db_unique=element[7]
				db_sibling=element[8]
				idgen=element[9]

			db_tx_rcv=int(db_tx_rcv)+1
			db_tx_sent=db_tx_sent
			db_amount_sent=db_amount_sent
			db_amount_rec=float(db_amount_rec)+float(json_obj['amount'])
			db_balance=float(db_amount_rec)-float(db_amount_sent)

			if(db_tx_rcv>1):
				db_unique=0
			else:
				db_unique=1

			
			query=("UPDATE transaction SET tx_rec=%s, amount_rec=%s, tx_sent=%s,amount_sent=%s,balance=%s,uniques=%s,sibling=%s,idgen=%s WHERE address=%s")            
			args = (db_tx_rcv,
			db_amount_rec,
			db_tx_sent,
			db_amount_sent,
			db_balance,
			db_unique,
			db_sibling,
			idgen,
			dd)

			cur.execute(query,args)
			db.commit() 
			print "*****************************************"
			print json_obj
