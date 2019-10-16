#Lib for mixers operations trought a socket
import socket
import json
from rpc_utils import *

def send_request(client,mixer_host,addr_fr,addr_to,velocity):
    if(len(addr_fr)>35):
        print("Your bitcoin address "+ addr_fr + " is too long.")
        return -1
    if(len(addr_to)>35):
        print("Your bitcoin address "+ addr_to + " is too long.")
        return -1
    addr_n=[]

    isvalid=rpc_call(client, mixer_host, 'validateaddress', "'" +addr_fr+"'")
    print(addr_fr + str(isvalid['isvalid']))
    if (not isvalid['isvalid']):
        print("Your bitcoin address "+ addr_fr + " not found in network.")
        return -1

    isvalid=rpc_call(client, mixer_host, 'validateaddress', "'" +addr_to+"'")
    print(addr_to + str(isvalid['isvalid']))

    if (not isvalid['isvalid']):
        print("Your bitcoin address "+ addr_to + " not found in network.")
        return -1

    print(mixer_host)
    
    data=send_request_mixer(mixer_host,addr_fr,addr_to,velocity)
    print(data)
    json_obj = json.loads(data)
    if(json_obj['address']=="-1"):
        print("Address already involved in a mixing...wait")
        return -1
    else:
        print("Send money to "+json_obj['address'])
        print("Mixing key secret "+json_obj['key'])
        return json_obj['address']


def send_request_mixer(host,addr_from,addr_to,velocity):
	# create a socket object
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	port = 9999
	# connection to hostname on the port.
	sock.connect((host, port))
	req ='{"from":"'+addr_from+'", "to":"'+addr_to+'","velocity":"'+velocity+'"}'

	sock.sendall(req)

	# Receive no more than 1024 bytes
	tm = sock.recv(1024)                                     
	sock.close()
	return tm

