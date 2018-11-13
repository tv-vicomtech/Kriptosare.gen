#!/bin/bash

/root/zcash/src/zcashd -datadir=/root/.zcash &

sleep 5

blocksci_parser --output-directory bitcoin-data update disk --coin-directory /root/.zcash/regtest/
cd /opt/BlockSci/Notebooks
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
