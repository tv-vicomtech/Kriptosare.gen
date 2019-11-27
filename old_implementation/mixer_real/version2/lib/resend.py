import socket
import time
import json
import rpc_utils
import datetime
import netifaces as ni

if __name__ == '__main__':
	client = docker.from_env()                          
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		             user="casino",         # your username
		             passwd="casino",  # your password
		             db="db")        # name of the data base
	db_list=[]
	mixer_server = "localhost"

	while True:
	    idlist=[]
	    cur = db.cursor()
	    query = ("SELECT * FROM casino where idca>%d")
	    if(len(db_list)>0):
	    	args = db_list[-1]['idex']
	    else:
		args=-1

	    cur.execute(query, args)

	    for element in cur.fetchall():
		db_list.extend(element)

	    for element in db_list:
	    	blkhash=rpc_call_blockhash(client,element['source'],blk,element['currencies'])
	    	blkinfo=rpc_call_blockinfo(client,element['source'],blkhash,element['currencies'])
		if(element['confirmations']>=blkinfo['confirmations']):
			payfee(element)
			rpc_call_sendmondey(client,mixer_server,element['destination'],element['amount'],element['currencies'])
			idlist.append(element['idca'])

			print "*****************************************"
	    		print "out to casino "+element['source']+":"+str(element['amount'])+str(element['currencies'])

	    db_list=[x for x in db_list if x["idca"] is not in idlist]
	    cur = db.cursor()
	    query = ("DELETE * FROM exchange WHERE idex==%d")
	    cur.execute(query, idlist)
	    time.sleep(10)

def payfee(element):
    r=randint(1,500)/10000
    element['amount']=round(element['amount']-(element['amount']*r),8)



