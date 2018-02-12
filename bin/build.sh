#!/bin/sh

set -e

GCLOUD_PROJECT_ID=etcdev
ORG=etcdev

function build {
    NAME=$1
    DOCKER=./docker/$NAME
    NAME_FULL=$ORG/ecip1041-$NAME
    echo "Build docker container for: $NAME_FULL from $DOCKER"

    docker build -t $NAME_FULL -f $DOCKER/Dockerfile .
}

function push {
    NAME=$1
    DOCKER_HUB=etcdev/ecip1041-$NAME

    docker tag $ORG/ecip1041-$NAME $DOCKER_HUB:latest
    gcloud docker -- push $DOCKER_HUB:latest
    #docker tag $ORG/ecip1041-$NAME $DOCKER_HUB:$VERSION
    #gcloud docker -- push $DOCKER_HUB:$VERSION
}

NAME=$1

echo "Build for $NAME"
echo "...................................................."

build $NAME
push $NAME

