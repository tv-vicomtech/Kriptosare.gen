import socket
import time
import json
from rpc_utils import *
import datetime
import docker
import MySQLdb
import numpy as np
from random import randint
from decimal import *

getcontext().prec = 8
looseall=35
loose=85

def shuffleodds(element):
	# 0 loose all, 1 loose something, 2 win 
	odds=randint(0,100)
	if(odds<looseall):
	    element[3]=0
	elif(odds<=loose):
	    r=randint(1,100)
	    value=float(r)/100
	    element[3]=round(float(element[3])*value,8)
	else:
	    r=randint(1,100)
	    value=float(r)/10
	    element[3]=round(float(element[3])*value,8)
	return odds

if __name__ == '__main__':
	client = docker.from_env()                          
    # name of the data base
	casino_server="localhost"
	db_list=[]
	idlist=[]

	while True:
	    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		             user="casino",         # your username
		             passwd="casino",  # your password
		             db="db") 
            #print("new")                     
	    cur = db.cursor()
	    query = ("SELECT * FROM casino where idca>%s")
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
	    for element in db_list:
	    	blkhash=rpc_call_blockhash(client,casino_server,str(element[5]),element[2])
	    	blkinfo=rpc_call_blockinfo(client,casino_server,blkhash,element[2])
	    	if(element[4]<=blkinfo['confirmations']):
	    		odds=shuffleodds(element)
	    		print "*****************************************"
	    		if(odds > looseall):
	    			balance = rpc_call_balance(client,casino_server,"btc")
	    			if(float(balance)>element[3]):
	    				destination=rpc_call_newaddress(client,element[1],element[2])
	    				rpc_call_sendmondey(client,casino_server,destination,str(element[3]),element[2])
	    				idlist.append(str(element[0]))
	    			else:
	    				print "this casino is poor"
	    		else:
	    			idlist.append(str(element[0]))


	    		print "out to casino "+element[1]+":"+str(element[3])+str(element[2])

	    db_list=[x for x in db_list if str(x[0]) not in idlist]
	    cur = db.cursor()
	    query = ("DELETE FROM casino WHERE idca in (%s)"% ','.join(["%s"] * len(idlist)))
	    if(len(idlist)>0):
	    	cur.execute(query, idlist)
	    	db.commit()
	    	for elem in idlist:
	    		idlist.remove(elem)
	    time.sleep(10)