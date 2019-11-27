import socket
import time
import json
import datetime
import MySQLdb
import numpy as np
from random import randint
from decimal import *
import subprocess 
import os 

def nodescan():
	list_el=[]
	for ping in range(1,15): 
		address = "172.192.0." + str(ping)
		devnull = open(os.devnull, 'w')
		res = subprocess.call(['ping', '-c', '1', address], stdout=devnull, stderr=devnull) 
		if res == 0: 
			list_el.append(address)
	return list_el


if __name__ == '__main__':
    # name of the data base
	miner_server="localhost"
	db_list=[]
	while True:
		db = MySQLdb.connect(host="localhost",    # your host, usually localhost
			user="pool",         # your username
			passwd="pool",  # your password
			db="db") 
            #print("new")                     
		cur = db.cursor()
		query = ("SELECT * FROM user")
		args=-1

		cur.execute(query)
		
		db_list=[]
		remove_el=[]

		for element in cur.fetchall():
			db_list.append(element[1])
		nodescan=nodescan()
		to_add=[]
		for jj in range(0,len(nodescan)):
			find =False
			if(nodescan[jj] in db_list):
				find=True
			if(not find):
				to_add.append(nodescan[jj])
		cur = db.cursor()
		query = ('INSERT INTO user (IP) values %s'% ','.join(['(%s)'] *len(to_add)))


		if(len(to_add)>0):
			values = [[item] for item in to_add]
			cur.execute(query, values)
			db.commit()
		time.sleep(300)
