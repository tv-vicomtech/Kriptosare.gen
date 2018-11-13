#!/bin/bash

bitcoind -rest -datadir=/root/.bitcoin &

sleep 5

blocksci_parser --output-directory bitcoin-data update disk --coin-directory /root/.bitcoin/regtest/


jupyter notebook --generate-config

sed -i 's/#c.NotebookApp.password = ''/c.NotebookApp.password = "sha1:ba6da2b4b678:4a43874b068856ba55d1eb704a82174cba515ee0"/g' /root/.jupyter/jupyter_notebook_config.py

cd /opt/BlockSci/Notebooks
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
