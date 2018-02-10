FROM ubuntu

RUN apt-get update && \
    apt-get -y install wget unzip git jq dnsutils netcat vim

ENV GETH_VER 4.0.0

RUN mkdir /opt/geth && \
    wget --progress=dot:mega https://github.com/ethereumproject/go-ethereum/releases/download/v${GETH_VER}/geth-classic-linux-v${GETH_VER}.tar.gz && \
    tar -zxf geth-classic-linux-v${GETH_VER}.tar.gz && \
    mv geth /usr/local/bin/ && \
    rm geth-classic-linux-v${GETH_VER}.tar.gz

RUN apt-get -y install python-pip python-setuptools python-dev && \
    pip install ecdsa && \
    pip install pysha3

RUN wget -O toxiproxy-2.1.2.deb --progress=dot:mega https://github.com/Shopify/toxiproxy/releases/download/v2.1.2/toxiproxy_2.1.2_amd64.deb && \
    dpkg -i toxiproxy-2.1.2.deb && \
    rm toxiproxy-2.1.2.deb

COPY docker/geth/start.sh /opt/geth/start.sh
COPY docker/geth/addpeers.sh /opt/geth/addpeers.sh
COPY docker/geth/ecip1041chain.json /opt/geth/ecip1041chain.json
COPY bin/ids.py /opt/geth/

RUN chmod +x /opt/geth/start.sh
RUN chmod +x /opt/geth/addpeers.sh

EXPOSE 8545
EXPOSE 30303
EXPOSE 30303/udp
EXPOSE 40404

WORKDIR /opt/geth

CMD ["/opt/geth/start.sh"]