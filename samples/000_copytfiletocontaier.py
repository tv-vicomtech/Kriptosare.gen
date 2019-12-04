import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *
import logging
import time
import subprocess

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()


if __name__ == '__main__':

    client = docker.from_env()

    fixname=DOCK_CONTAINER_NAME_PREFIX_BTC+"."

    nodelist = get_containers_names(client, DOCK_CONTAINER_NAME_PREFIX_BTC+".")

    #print("Wait 300 seconds...")
    #tool_bar(300)

    for uuid in nodelist:
        strn="docker exec "+str(uuid)+" rm /root/lib/generate_destination.py;"
        subprocess_cmd(strn)

        strn="docker cp /home/titanium/Kriptosare.gen/btc_testbed/lib/generate_destination.py "+str(uuid)+":/root/lib/"
        subprocess_cmd(strn)
        print(strn+"...changed")

    print("End!")