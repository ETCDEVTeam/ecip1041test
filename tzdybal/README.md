# Personal configuration and scripts for local deployment/testing

## Test Setup
1. 9 VMs, using VirtualBox, with Host Network Adapter (192.168.56.0/24).
   `kubemaster` was created and configured, and then cloned to get more instances. Remember to change MAC address of network adapter during cloning. 
1. Network:
```
192.168.56.1 host.testnet host
192.168.56.10 kubemaster.testnet kubemaster
192.168.56.11 kubeslave1.testnet kubeslave1
192.168.56.12 kubeslave2.testnet kubeslave2
192.168.56.13 kubeslave3.testnet kubeslave3
192.168.56.14 kubeslave4.testnet kubeslave4
192.168.56.15 kubeslave5.testnet kubeslave5
192.168.56.16 kubeslave6.testnet kubeslave6
192.168.56.17 kubeslave7.testnet kubeslave7
192.168.56.18 kubeslave8.testnet kubeslave8
```
1. `host` is a local development machine, where images are prepared and local docker registry is serving images
