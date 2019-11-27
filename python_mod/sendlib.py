import socket
import time
import datetime
import sys
from io import BytesIO

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

def send_to_node(client,source,destination,crypto,amount,ttime,host="localhost",port=9999):
	req =""
	source_ip=get_ip_by_unknown(client, source,DOCK_NETWORK_NAME_BTC)
	req ='{"source":"'+source_ip+'", "destination":"'+destination+'", "currencies":"'+crypto+'","amount":"'+str(amount)+'","time":"'+ttime.strftime("%Y-%m-%d %H:%M:%S")+'"}'
	print(req)
	server_ip=get_ip_by_unknown(client, host,DOCK_NETWORK_NAME_BTC)
	bytes_req = bytes(req, 'utf-8')
	send_(bytes_req,server_ip,port)

def ask_address(client,host="localhost",port=9998):
	req =""
	req ='{"source":"ciao"}'	
	server_ip=get_ip_by_unknown(client, host,DOCK_NETWORK_NAME_BTC)
	bytes_req = bytes(req, 'utf-8')
	aa=ask_(bytes_req,server_ip,port)
	return aa

def ask_(msg,host="localhost",port=9998):
	#host="localhost"
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	#port = 9999
	sock.connect((host, port))
	sock.sendall(msg)
	# Receive no more than 1024 bytes
	tm = sock.recv(1024)
	sock.close()
	return tm
