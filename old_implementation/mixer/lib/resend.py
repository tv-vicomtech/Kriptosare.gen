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

getcontext().prec = 8
looseall=35
loose=85

if __name__ == '__main__':
	client = docker.from_env()                          
    # name of the data base
	mixer_server="localhost"
	db_list=[]
	idlist=[]
	while True:
		db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		             user="mixer",         # your username
		             passwd="mixer",  # your password
		             db="db") 
            #print("new")                     
		cur = db.cursor()
		query = ("SELECT * FROM mixer where idmix>%s")
		if(len(db_list)>0):
			args = db_list[-1][0]
		else:
			args=-1
            #print db_list
		cur.execute(query, [args])
		for element in cur.fetchall():
			db_list.append(list(element))
		blkhash=""
 		blkinfo=""
		multirow=[]
		for element in db_list:
			blkhash=rpc_call_blockhash(client,mixer_server,str(element[7]))
			blkinfo=rpc_call_blockinfo(client,mixer_server,blkhash)

			if(int(blkinfo['confirmations'])==-1):
				idlist.append(str(element[0]))
			elif(int(blkinfo['confirmations'])>=int(element[5])):
				multirow.append([element[3],element[4]])
				idlist.append(str(element[0]))				

		if(len(multirow)>0):
			transactions_nout(client,multirow,mixer_server)


		db_list=[x for x in db_list if str(x[0]) not in idlist]
		cur = db.cursor()
		query = ("DELETE FROM mixer WHERE idmix in (%s)"% ','.join(["%s"] * len(idlist)))
		if(len(idlist)>0):
			cur.execute(query, idlist)
			db.commit()
			for elem in idlist:
				idlist.remove(elem)
		time.sleep(10)