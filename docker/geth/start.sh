#!/bin/bash

set -e

echo "-------------------------------------------------------"
echo "NODE  : $NODE_ID"
echo "PEERS : $NODE_PEERS"
echo "-------------------------------------------------------"

OPTS=""

python ids.py node-pk $NODE_ID > nodekey.txt
NODE_PK=$(python ids.py node-id $NODE_ID)
echo "ID: $NODE_PK"

NODE_IP=$(host $NODE_ID | awk '/has address/ { print $4 ; exit }')
echo "IP: $NODE_IP"

mkdir -p /data/ecip1017
cp ./ecip1017chain.json /data/ecip1017/chain.json

NODEADDR=$(python ids.py addr $NODE_ID)

OPTS="$OPTS --datadir /data"
OPTS="$OPTS --port 30303"
OPTS="$OPTS --rpc --rpcaddr 0.0.0.0"
OPTS="$OPTS --chain ecip1017"
#OPTS="$OPTS --bootnodes $BOOT --no-discover"
#OPTS="$OPTS --no-discover"
OPTS="$OPTS --nodekey nodekey.txt"
OPTS="$OPTS --etherbase $NODEADDR"
OPTS="$OPTS --nat extip:127.0.0.1"
#OPTS="$OPTS --verbosity 6"


#OPTS="$OPTS"

if [ "$NODE_MODE" == "miner" ]; then
    OPTS="$OPTS --mine"
fi

echo "-------------------------------------------------------"
echo "Setup network simulation"
echo "-------------------------------------------------------"

toxiproxy-server &
sleep 1
toxiproxy-cli create p2p -l 0.0.0.0:40404 -u localhost:30303
CONN_LATENCY=200
CONN_JITTER=100
if [ "$NODE_CONN" == "loose" ]; then
    CONN_LATENCY=700
    CONN_JITTER=300
fi
toxiproxy-cli toxic add p2p -t latency -a latency=${CONN_LATENCY} -a jitter=${CONN_JITTER}
toxiproxy-cli list

echo "-------------------------------------------------------"
echo "Run Geth:"
echo "    $OPTS"
echo "-------------------------------------------------------"

./addpeers.sh &
geth $OPTS