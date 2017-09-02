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

NODE_IP="0.0.0.0" #$(host $NODE_ID | awk '/has address/ { print $4 ; exit }')
echo "IP: $NODE_IP"

touch bootnodes.txt
while IFS=',' read -ra PEERS; do
    for name in ${PEERS[@]}; do
      PEER_ID=$(python ids.py node-id $name)
      PEER_HOST="$name"
      PEER_IP=$(host $PEER_HOST | awk '/has address/ { print $4 ; exit }')
      echo "enode://$PEER_ID@$PEER_IP:30303" >> bootnodes.txt
    done
done <<<  "$NODE_PEERS"

BOOTNODES=$(cat bootnodes.txt)
echo "PEERS:"
echo $BOOTNODES

NODEADDR=$(python ids.py addr $NODE_ID)

OPTS="$OPTS --base-path /data"
OPTS="$OPTS --rpc --rpcaddr 0.0.0.0"
OPTS="$OPTS --chain /opt/parity/ecip1017chain.json"
OPTS="$OPTS --no-discovery"
OPTS="$OPTS --reserved-only"
OPTS="$OPTS --reserved-peers bootnodes.txt"
OPTS="$OPTS --nodekey nodekey.txt"
OPTS="$OPTS --etherbase $NODEADDR"
OPTS="$OPTS --nat extip:$NODE_IP"
OPTS="$OPTS --logging trace"
OPTS="$OPTS --log-file /data/log.txt"
OPTS="$OPTS --rpc"
OPTS="$OPTS --jsonrpc-api parity,parity_set,eth,web3,net,traces,rpc,personal,parity_accounts"
OPTS="$OPTS --jsonrpc-cors *"

# if [ "$NODE_MODE" == "miner" ]; then
#     OPTS="$OPTS --mine"
# fi

echo "-------------------------------------------------------"
echo "Run Parity:"
echo "    $OPTS"
echo "-------------------------------------------------------"


/build/parity/target/release/parity $OPTS
