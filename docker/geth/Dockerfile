FROM golang:1.8-stretch

RUN apt-get update && \
    apt-get -y install wget unzip git jq dnsutils

RUN echo "GOPATH $GOPATH" && \
    mkdir -p /go/src/github.com/ethereumproject && \
    cd /go/src/github.com/ethereumproject && \
    git clone https://github.com/ethereumproject/go-ethereum.git && \
    cd go-ethereum && \
    git checkout monetary-policy && \
    go install ./cmd/geth && \
    rm -rf /go/src/github.com/ethereumproject

RUN apt-get -y install python-pip python-setuptools python-dev && \
    pip install ecdsa && \
    pip install pysha3

COPY docker/geth/start.sh /opt/geth/start.sh
COPY docker/geth/ecip1017chain.json /opt/geth/ecip1017chain.json
COPY bin/ids.py /opt/geth/

RUN chmod +x /opt/geth/start.sh

EXPOSE 8545
EXPOSE 30303
EXPOSE 30303/udp

WORKDIR /opt/geth

CMD ["/opt/geth/start.sh"]