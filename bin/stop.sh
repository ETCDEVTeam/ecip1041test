#!/bin/bash

kubectl delete rc node-g1-rc node-g2-rc node-g3-rc node-gm1-rc node-gm2-rc node-p1-rc node-p2-rc node-p3-rc node-pm1-rc
kubectl delete svc g1 g2 g3 gm1 gm2 p1 p2 p3 pm1

echo "Stopped. Wait for pods termination..."

kubectl get pods