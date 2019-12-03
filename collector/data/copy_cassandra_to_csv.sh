#!/bin/bash
COPY graphsense_raw.transaction to 'transaction.csv' with header=true;
COPY graphsense_raw.block to 'block.csv' with header=true;

docker cp datafeed_regtest:transaction.csv /home/titanium/Kriptosare.gen/extdata
docker cp datafeed_regtest:block.csv /home/titanium/Kriptosare.gen/extdata