from flask import Flask, render_template, request
import sys
import datetime
from wsgiref.simple_server import make_server

sys.path.insert(0, 'python_mod')
from docker_utils import *
from connection import *
from rpc_utils import *
from multirawtransaction import *
from btcconf import *
from zchconf import *

app = Flask(__name__)

global message_btc
global message_zch

@app.route('/')
def web_app():
	LOG_FILENAME = 'testbed'+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	LOG_FILENAME=LOG_FILENAME+".log"
	logging.basicConfig(filename="log/"+LOG_FILENAME,level=logging.INFO)

	return render_template('index.js', message_btc=[],message_zch=[])

@app.route('/transactionboard/')
def transactionboard():
	global message_btc
	global message_zch
	message_btc=[]
	message_zch=[]
	return render_template('transactionboard.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/comingback')
def comingback():
	global message_btc
	global message_zch
	message_btc=[]
	message_zch=[]
	return render_template('index.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/create_network', methods=['POST'])
def create_network():
	global message_btc
	global message_zch
	numbernodes=request.form['node']
	numberconn = 8
	cryptotype = request.form['label_create_network']
	message=[]
	client = docker_setup(cryptotype)
	if(cryptotype=="btc"):
		fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
		create_node(client, DOCK_NETWORK_NAME_BTC, cryptotype, numbernodes)
	elif(cryptotype=="zch"):
		fixname=DOCK_CONTAINER_NAME_PREFIX_ZCH+"."
		create_node(client, DOCK_NETWORK_NAME_ZCH, cryptotype, numbernodes)
	
	time.sleep(15)

	nodelist=get_containers_names(client, fixname)

	random_connection_container(client,nodelist,fixname,cryptotype, numberconn)

	message.append("********************")
	message.append(str(numbernodes)+" "+cryptotype+" created")

	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	return render_template('index_child.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/delete_network', methods=['POST'])
def delete_network():
	global message_btc
	global message_zch
	message=[]

	client = docker.from_env()
	cryptotype = request.form['label_remove_network']
	if(cryptotype=="btc"):
		remove_containers(client,DOCK_CONTAINER_NAME_PREFIX_BTC)
	if(cryptotype=="zch"):
		remove_containers(client,DOCK_CONTAINER_NAME_PREFIX_ZCH)
	message.append("********************")
	message.append("Network Deleted")
	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	return render_template('index_child.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/status_network', methods=['POST'])
def status_network():
	global message_btc
	global message_zch
	client = docker.from_env()
	nbtc=count_containers(client,DOCK_CONTAINER_NAME_PREFIX_BTC+".")
	nzch=count_containers(client,DOCK_CONTAINER_NAME_PREFIX_ZCH+".")
	nbtc_v = check_dock_dashboard(client,"btc")
	nzch_v = check_dock_dashboard(client,"zch")

	message_btc.append("*******************")
	message_btc.append(str(nbtc)+" BITCOIN nodes")
	message_btc.append(str(nbtc_v[0])+" BITCOIN statoshi")
	message_btc.append(str(nbtc_v[1])+" BITCOIN blocksci")
	message_btc.append(str(nbtc_v[2])+" BITCOIN graphsense")

	message_zch.append("*******************")
	message_zch.append(str(nzch)+" ZCASH nodes")
	message_zch.append(str(nzch_v[0])+" ZCASH statoshi")
	message_zch.append(str(nzch_v[1])+" ZCASH blocksci")
	message_zch.append(str(nzch_v[2])+" ZCASH graphsense")

	return render_template('index_child.js',message_btc=message_btc,message_zch=message_zch)

@app.route('/generate_blocks', methods=['POST'])
def generate_blocks():
	global message_btc
	global message_zch
	cryptotype=request.form['label_create_blk']
	opt_empty_random=request.form['opt_empty_random']
	num_to_gen=request.form['numtogen']
	client = docker.from_env()
	info=[]
	message=[]

	if(cryptotype=="btc"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")
	elif(cryptotype=="zch"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_ZCH+".")
	if(int(num_to_gen)>0):
		if(opt_empty_random=="E"):
			info=mining_blocks(client,nodelist[0],cryptotype,int(num_to_gen))

		elif(opt_empty_random=="R"):
			info=generaterandomtransaction(client,nodelist,cryptotype,int(num_to_gen))

	else:
		if(opt_empty_random=="Y"):
			info=send_money_to_all(client,nodelist,cryptotype)
		else:
			info.append("No blocks created")

	message.append("********************")
	message.extend(info)
	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	return render_template('tx_child.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/status_blockchain', methods=['POST'])
def status_blockchain():
	global message_btc
	global message_zch
	message=[]
	cryptotype=request.form['label_status_blk']
	client = docker.from_env()
	if(cryptotype=="btc"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")
	elif(cryptotype=="zch"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_ZCH+".")

	information=getinfoblockchainfrom(client,nodelist,cryptotype)

	message.append("********************")
	message.append(cryptotype+" INFO")
	message.extend(information)
	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	return render_template('tx_child.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/get_info', methods=['POST'])
def get_info():
	global message_btc
	global message_zch
	message=[]
	information=[]
	cryptotype=request.form['label_get_info']
	whichinfo=request.form['opt_info']
	contnumb=request.form['contnumb']
	client = docker.from_env()
	if(cryptotype=="btc"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+"."+contnumb)
	elif(cryptotype=="zch"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_ZCH+"."+contnumb)

	message.append("********************")
	if(len(nodelist)>0):
		if(whichinfo=="A"):
			information=getinfowalletfrom(client,nodelist[0],cryptotype)
		elif(whichinfo=="N"):
			information=getnewaddressfrom(client,nodelist[0],cryptotype)
		elif(whichinfo=="L"):
			information=listunspentfrom(client,nodelist[0],cryptotype)
		message.append("Node Index "+contnumb+" = "+nodelist[0]+":")
	else:
		information.append("Node with Index "+contnumb+" not found")

	message.extend(information)
	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	return render_template('tx_child.js', message_btc=message_btc,message_zch=message_zch)


@app.route('/listnode', methods=['POST'])
def listnode():
	global message_btc
	global message_zch
	message=[]
	message.append("********************")
	page=""
	cryptotype=request.form['label_list_node']
	whatpage=request.form['whatpage']
	client = docker.from_env()
	if(cryptotype=="btc"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")
	elif(cryptotype=="zch"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_ZCH+".")

	if(len(nodelist)<0):
		message.append("Node with Index "+contnumb+" not found")
	else:
		for i in range(0,len(nodelist)):
			message.append("# "+str(i+1)+" => name: "+ nodelist[i])

	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	#print whatpage
	if(whatpage=="1"):
		page='index_child.js'
	elif(whatpage=="2"):
		page='tx_child.js'
	#print page
	return render_template(page, message_btc=message_btc,message_zch=message_zch)

@app.route('/control_gen', methods=['POST'])
def control_gen():
	global message_btc
	global message_zch
	client = docker.from_env()
	message=[]

	cryptotype=request.form['label_control_gen']
	fromaddress=request.form['fromaddress']
	toaddress=request.form['toaddress']
	amount=request.form['amount']

	if(cryptotype=="btc"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+"."+fromaddress)
	elif(cryptotype=="zch"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_ZCH+"."+fromaddress)

	message.append("********************")
	
	if(len(nodelist)>0):
		source=nodelist[0]
		info = send_to_address(client,source,amount,toaddress,cryptotype)
		message.extend(info)
	else:
		message.append("Node with index "+fromaddress+" not found")

	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	return render_template('tx_child.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/mining_gen', methods=['POST'])
def mining_gen():
	global message_btc
	global message_zch
	client = docker.from_env()
	message=[]

	cryptotype=request.form['label_mining_gen']

	if(cryptotype=="btc"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")
	elif(cryptotype=="zch"):
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_ZCH+".")

	message.append("********************")
	
	if(len(nodelist)>0):
		rand = randint(0,len(nodelist))
		source=nodelist[rand]
		info = mining_blocks(client,source,cryptotype,1)
		message.extend(info)
	else:
		message.append("Node not present for mining")

	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	return render_template('tx_child.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/create_dash', methods=['POST'])
def create_dash():
	global message_btc
	global message_zch
	checkbox1=request.form.get('statoshi')
	checkbox2=request.form.get('blocksci')
	checkbox3=request.form.get('graphsense')
	cryptotype=request.form['label_create_dash']
	message=[]
	check=False

	if(checkbox1=="S"):
		check=True
		info=generate_statoshi(cryptotype)
		message.extend(info)
	if(checkbox2=="B"):
		check=True
		info=generate_blocksci(cryptotype)
		message.extend(info)
	if(checkbox3=="G"):
		check=True
		info=generate_graphsense(cryptotype)
		message.extend(info)
	if(not check):
		message.append("********************")
		message.append("No tools created")

	if(cryptotype=="btc"):
		message_btc.extend(message)
	elif(cryptotype=="zch"):
		message_zch.extend(message)
	return render_template('index_child.js', message_btc=message_btc,message_zch=message_zch)

@app.route('/remove_dashboard', methods=['POST'])
def remove_dashboard():
	global message_btc
	global message_zch
	client = docker.from_env()
	cryptotype=request.form['label_remove_dash']
	message=[]
	message.append("********************")
	if(cryptotype=="btc"):
		nbtc = check_dock_dashboard(client,"btc")
		remove_dock_dashboard(client,"btc")
		message_btc.extend(message)
		message_btc.append(str(nbtc)+" BTC containers removed [Statoshi, Blocksci, Graphsense]")
	elif(cryptotype=="zch"):
		nzch = check_dock_dashboard(client,"zch")
		remove_dock_dashboard(client,"zch")
		message_zch.extend(message)
		message_zch.append(str(nzch)+" ZCH containers removed [Statoshi, Blocksci, Graphsense]")
	return render_template('index_child.js', message_btc=message_btc,message_zch=message_zch)

def generate_blocksci(cryptotype="btc"):
	global message_btc
	global message_zch
	message=[]

	if(cryptotype=="btc"):
		client=blocksci_setup(True, True, cryptotype)
	#elif(cryptomoney=="zch"):
		#client=blocksci_setup(True, True, cryptotype="zch")
	generate_dock_blocksci(client,cryptotype)

	if(cryptotype=="btc"):
		fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
		nodelist=get_containers_names(client, fixname)
	#elif(cryptotype=="zch"):
	#	fixname=DOCK_CONTAINER_NAME_PREFIX_ZCH+"."
	#	nodelist=get_containers_names(client, fixname)
	time.sleep(5)

	if(cryptotype=="btc"):
		random_connection_element(client,nodelist,DOCK_MACHINE_NAME_BLOCKSCI_BTC,fixname,cryptotype)
	#elif(cryptotype=="zch"):
	#	random_connection_dash(client,nodelist,DOCK_MACHINE_NAME_BLOCKSCI_BTC,num_conn)
	message.append("********************")
	message.append("Blocksci ready")
	return message

def generate_statoshi(cryptotype="btc"):
	global message_btc
	global message_zch
	message=[]

	if(cryptotype=="btc"):
		client=statoshi_setup(True, True, cryptotype)
	#elif(cryptomoney=="zch"):
		#client=statoshi_setup(True, True, cryptotype="zch")
	generate_dock_statoshi(client,cryptotype)

	if(cryptotype=="btc"):
		fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
		nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")
	#elif(cryptotype=="zch"):
	#	fixname=DOCK_CONTAINER_NAME_PREFIX_ZCH+"."
	#	nodelist=get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_ZCH+".")

	if(len(nodelist)>9):
		num_conn=8
	else:
		num_conn=len(nodelist)
	time.sleep(5)

	if(cryptotype=="btc"):
		random_connection_element(client,nodelist,DOCK_IMAGE_NAME_STATOSHI,fixname,cryptotype)
	#elif(cryptotype=="zch"):
	#	random_connection_dash(client,nodelist,DOCK_IMAGE_NAME_STATOSHI,num_conn)
	message.append("********************")
	message.append("Statoshi ready")
	return message


def generate_graphsense(cryptotype="btc"):
	global message_btc
	global message_zch
	message=[]

	if(cryptotype=="btc"):
		client=grph_setup(True, True, cryptotype)
		fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."
	elif(cryptotype=="zch"):
		client=grph_setup(True, True, cryptotype)
		fixname=DOCK_CONTAINER_NAME_PREFIX_ZCH+"."

	generate_dock_grph(client,cryptotype)
	nodelist=get_containers_names(client, fixname)

	if(len(nodelist)>9):
		num_conn=8
	else:
		num_conn=len(nodelist)
	time.sleep(5)
	if(cryptotype=="btc"):
		random_connection_element(client,nodelist,DOCK_IMAGE_NAME_CLIENT_BTC,fixname,cryptotype)
	elif(cryptotype=="zch"):
		random_connection_element(client,nodelist,DOCK_IMAGE_NAME_CLIENT_ZCH,fixname,cryptotype)

	message.append("********************")
	message.append("Graphsense "+cryptotype+" ready")
	return message


def getinfoblockchainfrom(client,nodelist,cryptotype="btc"):
    strg=[]
    n=0
    n=rpc_call_blockcount(client,nodelist[0],cryptotype)
    num=str(n)
    strg.append("- Number of Block: "+num)
    hash_last=rpc_call_blockhash(client,nodelist[0],num,cryptotype)
    strg.append("- Last Block hash: "+hash_last)
    tx_last=rpc_call_blockinfo(client,nodelist[0],hash_last,cryptotype)
    strg.append("- Block confirmation: "+str(tx_last['confirmations']))
    strg.append("- Block size: "+str(tx_last['size']))
    strg.append("- Block num. tx: "+str(len(tx_last['tx'])))
    strg.append("- Block time: "+str(tx_last['time']))
    return strg

def getinfowalletfrom(client,nodename,cryptotype="btc"):
    strg=[]
    walletinfo=rpc_call_walletinfo(client,nodename,cryptotype)
    strg.append("- Balance: "+str(walletinfo['balance']))
    strg.append("- Tx count: "+str(walletinfo['txcount']))
    strg.append("- Pay tx fee: "+str(walletinfo['paytxfee']))
    address_account=rpc_call_accountaddress(client,nodename,cryptotype)
    strg.append("- Address account:"+str(address_account))

    return strg

def getnewaddressfrom(client,nodename,cryptotype="btc"):
    strg=[]
    new_address=rpc_call_newaddress(client,nodename,cryptotype)
    strg.append("New address: "+str(new_address))

    return strg

def listunspentfrom(client,nodename,cryptotype="btc"):
    strg=[]
    listunspent=""
    listunspent=rpc_call_listunspent(client,nodename,cryptotype)

    if(len(listunspent)==0):
    	strg.append("Unspent tx not present")
    else:
        for i in range(0,len(listunspent)):
            strg.append("##."+str(i+1))
            strg.append("- txid: "+str(listunspent[i]['txid']))
            strg.append("- vout: "+str(listunspent[i]['vout']))
            strg.append("- address: "+str(listunspent[i]['address']))
            strg.append("- amount: "+str(listunspent[i]['amount']))
            strg.append("- confimations: "+str(listunspent[i]['confirmations']))

    return strg


if __name__ == '__main__':
	message_btc=[]
	message_zch=[]
	app.run(host="0.0.0.0",port=8811)
