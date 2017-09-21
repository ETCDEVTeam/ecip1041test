#!/bin/bash

set -e

sleep 10
echo "Adding peers: $NODE_PEERS"

touch peers.js
while IFS=',' read -ra PEERS; do
    for name in ${PEERS[@]}; do
      PEER_ID=$(python ids.py node-id $name)
      PEER_HOST="$name"
      PEER_IP=$(host $PEER_HOST | awk '/has address/ { print $4 ; exit }')
      echo "admin.addPeer('enode://$PEER_ID@$PEER_IP:30303');" >> peers.js
    done
done <<<  "$NODE_PEERS"

OPTS="--datadir /data --chain ecip1017"

geth $OPTS --exec "loadScript('peers.js')" attach