#!/usr/bin/env python

# pip install kubernetes

import json
from pprint import pprint
import rpc_api

all_nodes = ["g1", "g2", "gm1"]

def same_fork(hashes):
    return len(set(hashes)) == 1

def find_fork(api, pods, no_fork_at, fork_at):
    check_height = no_fork_at + int((fork_at - no_fork_at) / 2)
    hashes = [api.get_hash(pod_id, hex(check_height))["hash"] for pod_id in pods]
    if not same_fork(hashes):
        return find_fork(api, pods, no_fork_at, check_height)
    else:
        gap = check_height - no_fork_at
        if gap > 1:
            return find_fork(api, pods, check_height, fork_at)
        else:
            return check_height + 1

def check_fork():
    print("Checking for a fork...")
    api = rpc_api.RpcApi()
    pods = api.get_nodes()
    min_height = min([int(api.get_height(pod_id), 16) for pod_id in pods]) - 10
    if min_height <= 0:
        print("Ok. Blockchain has less than 10 blocks")
        return 
    hashes = [api.get_hash(pod_id, hex(min_height))["hash"] for pod_id in pods]
    if not same_fork(hashes):
        print("!!!! Fork detected !!!!")
        fork_block = find_fork(api, pods, 0, min_height)
        print("Fork happened at %s" % fork_block)
        print("%s\t\t\t%s\t%s" % ("ID", "HEIGHT", "HASH"))
        for pod_id in pods:
            hash = api.get_hash(pod_id, fork_block)["hash"]
            print("%s\t%s\t%s" % (pod_id, fork_block, hash))
    else:
        print("Ok. No Fork detected")


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
    check_fork()
