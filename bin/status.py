#!/usr/bin/env python

# pip install kubernetes

import json
from pprint import pprint
import rpc_api

all_nodes = ["g1", "g2", "gm1"]

def list():
    print("Nodes status")
    print("%s\t\t\t%s\t%s\t%s" % ("ID", "PEERS", "HEIGHT", "HASH"))
    api = rpc_api.RpcApi()
    pods = api.get_nodes()
    for pod_id in pods:
        height = api.get_height(pod_id)
        hash = api.get_hash(pod_id, height)["hash"]
        peers = api.get_peers(pod_id)
        print("%s\t%s\t%s\t%s" % (pod_id, int(peers, 16), int(height, 16), hash))

if __name__ == "__main__":
    list()
