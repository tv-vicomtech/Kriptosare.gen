# Testbed Vicomtech

## Multi-cryptocurrencies dataset generator
Sometimes, real world test-data may not reflect known or emerging criminal threats or simply are not enough or are too expensive.
This repo contain a dockerized bitcoin-zcash testbed as a private custom-made network for generating synthetic datasets. The aim of the synthetic dataset is to fill a current need to use privacy-aware data that allows us to develop algorithms for blockchain analysis in a controlled environment.
With this tool is possible recreate network by coding or directly reading a grphml file. Mining blocks, generate transactions, and set all the parameters in order to control the whole network
The created network is totally separated from the Mainnet and the Testnet. In there are integrated also some third-tools for analyzing the simulated blockchain.

This tool is implemented in European TITANIUM project H2020.

## Software Requirement and conditions
### Python 2.7.12
All the scripts used for creating the dockerized bitcoin testbed are developed in Python2. The scripts are automated and with them is possible to define the network design. Python is a programming language that lets you work more quickly and integrate your systems more effectively.
https://docs.python.org/2/index.html

### Docker version 17.12.1-ce, build 7390fc6
The testbed is a completely dockerized system, so, the first requirement is the Docker presence. Docker is a platform that allows us to create ‘containers’, in which all the required software is included. Containerized software will always run the same code, regardless of the environment, ensuring high portability and easy setup. The testbed creates containers as much as there are bitcoin users, so that each container represents a real user/wallet. In each container node, a bitcoin daemon is running with defined network parameters (in order to simulate individual user behaviour). Each node is linked to others, forming a peer-to-peer network.
https://docs.docker.com/

### Docker swarm
In order to implement a certain bitcoin transactions scenario, we need to recreate an environment similar to the real bitcoin network, in which there are a lot of peer-to-peer nodes that carries out multiple user operations. To achieve this, it is possible to implement the core network using Docker Swarm. A Docker Swarm cluster consists of a Docker Engine deployed on multiple servers. To deploy an application image when Docker Engine is in Swarm mode, a service is created. The Swarm architecture allows us to divide computing efforts among workers by including a manager node. Manager nodes perform orchestration and cluster management, while worker nodes receive and execute tasks controlled by the manager.
https://docs.docker.com/engine/swarm/swarm-tutorial/

## Installation Guide
OS: Ubuntu 16.04 Operative System (xenial)
Step 1: Installation of  Python 2.7.12.
```
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
cd ~/Downloads 
wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz
tar -xvf Python-2.7.12.tgz
cd Python-2.7.12
./configure
sudo make install
```
Step 2: Installation of Docker version 17.12.1-ce
```
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add –
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \ "deb [arch=amd64] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) \stable"
sudo apt-get update
sudo apt-get install docker-ce=17.12.1~ce-0~ubuntu
docker ps
sudo apt-get install pip
sudo pip install flask
sudo pip install python-bitcoinrpc docker==2.7.0
```

Step 4: Download the Testbed code from this repository
Ones that all the software are installed, download the Testbed project:
```
git clone git@gitlab.vicomtech.es:TITANIUM_EU9256_2016/TITANIUM-Testbed.git
```
Now you are ready to create your own dockerized bitcoin network

## Network configuration
In the project there are two configuration files that you can change according to your networks parameters. Go in the folder:
```
cd /TITANIUM/testbed/python_mod
```
and there you can find btcconf.py and zchcconf.py.


## Getting Started

The execution of a simulation needs to be main placed in this folder:
 /TITANIUM/testbed
 
### End-user
So if you want to start the user interface you have to go in this folder and execute in a terminal
```
python web_app.py
```
After executing you have to open your browser and type the ip of your server (or localhost if you run the script locally) and the port :8811
[ip]:8811
Now the interface is ready.

### Developer
If you want create your own scenario and execute it in an automatic script and play with the libraries availables you have to create a script in the folder
/TITANIUM/testbed
and run it with
```
python nameofscript.py
```
You can find some example script in the folder
```
> cd /TITANIUM/testbed/samples
```
### ATTENTION
All dockerized image tools are previously compiled and each tool download them from a docker HUB, however if you figure out an error, or just want compile the image for your own, in each "folder tools" you can find a Docker_complete file.
(This can increase the time of execution on the basis of server feature and the needed tools)
