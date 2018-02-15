#!/bin/bash

set -e

kubectl create -f ./k8s/nodes.svc.yaml
kubectl create -f ./tzdybal/k8s/nodes.rc.yaml

echo Please give 2-3 minutes to spin up nodes before calling bin/status.py
