import socket
import time
import datetime
import sys
sys.path.insert(0, '../python_mod')

from docker_utils import *

def send_(msg,host="localhost",port=9999):
	#host="localhost"
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	#port = 9999
	# connection to hostname on the port.
	sock.connect((host, port))
	sock.sendall(msg)
	# Receive no more than 1024 bytes
	#tm = sock.recv(1024)                                     
	sock.close()

def send_to_mixer(client,source,crypto,amount,ttime,host="localhost",port=9999,destination=None):
	req =""
	source_ip=get_ip_by_unknown(client, source,DOCK_NETWORK_NAME_BTC)
	req ='{"source":"'+source_ip+'", "currencies":"'+crypto+'","amount":"'+str(amount)+'","time":"'+ttime.strftime("%Y-%m-%d %H:%M:%S")+'"}'
	#print req
	server_ip=get_ip_by_unknown(client, host,DOCK_NETWORK_NAME_BTC)
	send_(req,server_ip,port)

def send_to_exchange(client,source,destination,fromcrypto,tocrypto,amount,ttime,host="localhost",port=9999):
	req =""
	if(fromcrypto=="btc"):
		source_ip=get_ip_by_unknown(client, source,DOCK_NETWORK_NAME_BTC)
	elif(fromcrypto=="zch"):
		#source_ip=get_ip_by_unknown(client, source,DOCK_NETWORK_NAME_ZCH)
		source_ip=get_ip_by_unknown(client, source,DOCK_NETWORK_NAME_BTC)

	req ='{"source":"'+source_ip+'","destination":"'+destination+'", "fromcurrencies":"'+fromcrypto+'", "tocurrencies":"'+tocrypto+'","amount":"'+str(amount)+'","time":"'+ttime.strftime("%Y-%m-%d %H:%M:%S")+'"}'
	
	#print req
	server_ip=get_ip_by_unknown(client, host, DOCK_NETWORK_NAME_BTC)
	send_(req,server_ip,port)

def send_to_casino(client,source,crypto,amount,ttime,host="localhost",port=9999):
	req =""
	source_ip=get_ip_by_unknown(client, source,DOCK_NETWORK_NAME_BTC)
	req ='{"source":"'+source_ip+'", "currencies":"'+crypto+'","amount":"'+str(amount)+'","time":"'+ttime.strftime("%Y-%m-%d %H:%M:%S")+'"}'
	#print req
	server_ip=get_ip_by_unknown(client, host,DOCK_NETWORK_NAME_BTC)
	send_(req,server_ip,port)
