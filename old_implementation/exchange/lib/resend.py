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

rate_zch_btc=51

if __name__ == '__main__':
	client = docker.from_env()                          
    # name of the data base
	exchange_server="localhost"
	db_list=[]
	idlist=[]
	while True:
	    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		             user="exchange",         # your username
		             passwd="exchange",  # your password
		             db="db") 
            #print("new")                     
	    del idlist[:]
	    cur = db.cursor()
	    query = ("SELECT * FROM exchange where idex>%s")
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
	    	if(element[3]=="zch"):
		    	blknum=rpc_call_blockcount(client,exchange_server,element[4])
		    	blkhash=rpc_call_blockhash(client,exchange_server,str(element[7]),element[4])
		    	blkinfo=rpc_call_blockinfo(client,exchange_server,blkhash,element[4])
		    	if(element[6]<=blkinfo['confirmations']):
		    		#print "*****************************************"
		    		amount_rated=0
		    		balance = rpc_call_balance(client,exchange_server,element[4])
		    		if(element[4]=="btc"):
		    			amount_rated=round(float(element[5])*(1.0/rate_zch_btc),8)

	    			if(float(balance)>float(amount_rated)):
	    				destination=element[2]
	    				rpc_call_sendmondey(client,exchange_server,destination,str(amount_rated),element[4])
	    				print "node "+element[1]+" change: "+str(element[5])+" "+element[3]+" to "+str(amount_rated)+" "+element[4]
	    				idlist.append(str(element[0]))
	    			else:
	    				print "this exchange is poor"
		    	else:
		    		print "blockchain not ready or connection problem"
		else:
		    	blknum=rpc_call_blockcount(client,exchange_server,"btc")
		    	blkhash=rpc_call_blockhash(client,exchange_server,str(element[7]),"btc")
		    	blkinfo=rpc_call_blockinfo(client,exchange_server,blkhash,"btc")
		    	if(int(element[6])<=blkinfo['confirmations']):
		    		#print "*****************************************"
		    		idlist.append(str(element[0]))

	    db_list=[x for x in db_list if str(x[0]) not in idlist]
	    print db_list

	    cur = db.cursor()
	    query = ("DELETE FROM exchange WHERE idex in (%s)"% ','.join(["%s"] * len(idlist)))
	    if len(idlist)>0:
	    	cur.execute(query, idlist)
	    	db.commit()
	    time.sleep(10)