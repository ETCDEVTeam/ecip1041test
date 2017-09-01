#
# Gets all blocks from first to latest, builds an expected distribution of ether at the end, and
# verifies that it's equal to the state of chain
#

import status
import math
from collections import defaultdict
import rpc_api

ETHER = math.pow(10, 18)

def hr():
    print("-------------------------------------------")

def toEther(wei):
    return long(wei, 16) / ETHER

def toWei(ether):
    val = long(ether * ETHER)
    return val

def toWeiHex(ether):
    return toWei(ether).rstrip('L')

def coef(x, i):
    if i == 0:
        return x
    return coef(x * 0.8, i - 1)

class Era:
    def __init__(self, num):
        self.era = int(math.floor((num - 1) / 500))

    def get_block_reward(self):
        return toWei(coef(5.0, self.era))

    def get_uncle_miner_reward(self, uncle_height, height):
        if self.era == 0:
            d = 8 + uncle_height - height
            return toWei(5) * d / 8
        return toWei(coef(0.125, self.era))

    def get_uncle_finder_reward(self):
        if self.era == 0:
            return toWei(5) / 32
        return toWei(coef(0.125, self.era))

class ChainState:
    def __init__(self, api):
        self.api = api
        self.nodes = self.api.get_nodes()
        self.height = min(int(api.get_height(self.nodes[0]), 16), 1501)

    def download(self):
        hr()
        print("Download blockchain for local analysis.... (blocks 1..%s, it may take 5+ minutes)" % self.height)
        nodes_count = len(self.nodes)
        get_block = lambda num: self.api.get_block(self.nodes[0], num)
        blocks = map(get_block, range(1, self.height + 1))
        blocks_w_uncles = filter(lambda b: len(b["uncles"]) > 0, blocks)
        get_uncles = lambda block: self.api.get_uncles(self.nodes[0], block)
        self.uncles = map(get_uncles, blocks_w_uncles)
        #print("uncles: %s" % self.uncles)
        self.state = reduce(reduce_state, blocks, defaultdict(lambda: 0))
        self.state = reduce(reduce_uncles_state, self.uncles, self.state)
        self.stats_blocks = reduce(reduce_to_blocks, blocks, defaultdict(lambda: 0))
        self.stats_uncles_found = reduce(reduce_to_uncles, blocks, defaultdict(lambda: 0))
        self.stats_uncles_made = reduce(reduce_to_uncles_made, self.uncles, defaultdict(lambda: 0))
        print "Done"
        hr()

    def display(self):
        hr()
        print("Mining stats:")
        for miner, block_count in self.stats_blocks.items():
            print("  Miner %s made %s blocks" % (miner, block_count))
        for miner, uncles_count in self.stats_uncles_found.items():
            print("  Miner %s found %s uncles" % (miner, uncles_count))
        for miner, uncles_count in self.stats_uncles_made.items():
            print("  Miner %s made %s uncles" % (miner, uncles_count))
        hr()
        print("Expected state:")
        for miner, balance in self.state.items():
            print("  Miner %s should have %s" % (miner, balance))
        hr()

    def verify(self):
        has_problem = False
        hr()
        print("Verifying...")
        for miner, balance in self.state.items():
            act = api.rpc_call(self.nodes[0], "eth_getBalance", [miner, hex(self.height)])
            if abs(toEther(hex(balance)) - toEther(act)) > 0.0001:
                has_problem = True
                print("Invalid balance for miner %s: %s != %s (exp != act)" % (miner, toEther(hex(balance)), toEther(act)))
                print("                %s wei != %s wei" % (hex(balance).rstrip('L'), act))
        if not has_problem:
            print "  OK. Blockchain has a valid state"
        hr()

def reduce_state(state, block):
    miner = block["miner"]
    base = state[miner]
    era = Era(int(block["number"], 16))
    #print("era %s at %s with %s" % (era.era, int(block["number"], 16), era.get_block_reward()))
    base += era.get_block_reward()
    for uncle in block["uncles"]:
        finder_reward = era.get_uncle_finder_reward()
        #print("Reward miner %s with %s at era %s" % (miner, finder_reward / ETHER, era.era))
        base += finder_reward
    state[miner] = base
    return state

def reduce_uncles_state(state, block_uncles):
    for block in block_uncles:
        height = int(block[0], 16)
        era = Era(height)
        uncle = block[1]
        miner = uncle["miner"]
        reward = era.get_uncle_miner_reward(int(uncle["number"], 16), height)
        #print("Reward miner %s with %s at era %s at dist %s..%s" % (miner, reward / ETHER, era.era, height, int(uncle["number"], 16)))
        state[miner] += reward
    return state


def reduce_to_blocks(stats_blocks, block):
    miner = block["miner"]
    stats_blocks[miner] += 1
    return stats_blocks

def reduce_to_uncles(stats, block):
    miner = block["miner"]
    stats[miner] += len(block["uncles"])
    return stats

def reduce_to_uncles_made(stats, block_uncles):
    for block in block_uncles:
        uncle = block[1]
        miner = uncle["miner"]
        stats[miner] += 1
    return stats

if __name__ == '__main__':
    print("Verify blockchain state....")
    api = rpc_api.RpcApi()
    state = ChainState(api)
    state.download()
    state.display()
    state.verify()
