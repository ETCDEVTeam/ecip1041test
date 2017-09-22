#!/bin/bash

set -e

PROJECT_ID=$1
PROJECT_ZONE=$2
PROJECT_CLUSTER=$3

gcloud config set project $PROJECT_ID
gcloud config set compute/zone $PROJECT_ZONE
gcloud config set container/cluster $PROJECT_CLUSTER
gcloud container clusters get-credentials $PROJECT_CLUSTER

kubectl create -f ./k8s/nodes.svc.yaml
kubectl create -f ./k8s/nodes.rc.yaml

echo Please give 2-3 minutes to spin up nodes before calling bin/status.py