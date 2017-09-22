#!/bin/bash

kubectl delete rc node-gm1-rc node-gm2-rc
kubectl delete rc node-g1-rc node-g2-rc node-g3-rc
kubectl delete rc node-p1-rc node-p2-rc node-p3-rc
kubectl delete svc gm1 gm2 g1 g2 g3 g4 p1 p2 p3

echo "Stopped. Wait for pods termination..."

kubectl get pods