import sys

sys.path.insert(0, '../python_mod')
from docker_utils import *
from btcconf import *
from rpc_utils import *
from connection import *

import logging
from random import randint
import time
import datetime
from getopt import getopt
from mysocket import *
import subprocess

def tool_bar(tt):
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * tt))
    sys.stdout.flush()
    sys.stdout.write("\b" * (tt+1)) # return to start of line, after '['

    for i in range(tt):
        time.sleep(1) # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n") # this ends the progress bar

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
        strn="docker exec -d "+str(uuid)+" nohup python /root/lib/generate_destination.py;"
        subprocess_cmd(strn)
        print(strn+"...started")

    print("End!")
