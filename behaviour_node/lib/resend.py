import socket
import time
import json
from rpc_utils import *
from multirawtransaction import *
import datetime
import docker
import MySQLdb
import numpy as np
from random import randint
from decimal import *
import subprocess 
from collections import Counter

getcontext().prec = 8
looseall=35
loose=85

if __name__ == '__main__':
	client = docker.from_env()                          
    # name of the data base
	miner_server="localhost"
	db_list=[]
	remove_el=[]
	while True:
		db = MySQLdb.connect(host="localhost",    # your host, usually localhost
			user="vicom",         # your username
			passwd="vicom",  # your password
			db="db") 
            #print("new")                     
		cur = db.cursor()
		query = ("SELECT * FROM received_tx where idrecv>%s")
		args=-1

		cur.execute(query, [args])
		
		db_list=[]
		add_list=[]
		remove_el=[]

		for element in cur.fetchall():
			db_list.append(list(element))
			add_list.append(element[2])

		blkinfo=""
		multirow=[]

		cur = db.cursor()
		query = ("SELECT * FROM user")
		nodescan=[]
		cur.execute(query)
		for element in cur.fetchall():
			nodescan.append(element[1])

		if(db_list>0 and nodescan>0):
			for element in db_list:
				if(element[2] not in remove_el):
					blkhash=rpc_call_blockhash(client,miner_server,str(element[6]))
					blkinfo=rpc_call_blockinfo(client,miner_server,blkhash)
					if(blkinfo['confirmations']==-1):
						pass
					elif(blkinfo['confirmations']>=element[5]):
						#destination=rpc_call_newaddress(client,nodescan[ii],element[3])
						cnt=0
						for gg in add_list:
							if(gg==element[2]):
								cnt=cnt+1
						multirow.append([nodescan,element[2],cnt])
						remove_el.append(str(element[2]))


			for jj in range(0,len(multirow)):
				transactions_nout(client,multirow[jj],miner_server)

			cur = db.cursor()
			query = ("DELETE FROM received_tx WHERE destination in (%s)"% ','.join(["%s"] * len(remove_el)))
			if(len(remove_el)>0):
				cur.execute(query, remove_el)
				db.commit()
		time.sleep(10)