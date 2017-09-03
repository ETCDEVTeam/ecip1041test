FROM parity/parity:v1.7.2

RUN apt-get update && \
    apt-get -y install wget unzip jq dnsutils

RUN apt-get -y install python python-pip python-setuptools python-dev && \
    pip install ecdsa && \
    pip install pysha3

RUN wget -O toxiproxy-2.1.2.deb --progress=dot:mega https://github.com/Shopify/toxiproxy/releases/download/v2.1.2/toxiproxy_2.1.2_amd64.deb && \
    dpkg -i toxiproxy-2.1.2.deb

COPY docker/parity/start.sh /opt/parity/start.sh
COPY docker/parity/ecip1017chain.json /opt/parity/ecip1017chain.json
COPY bin/ids.py /opt/parity/

RUN chmod +x /opt/parity/start.sh

EXPOSE 8545
EXPOSE 30303
EXPOSE 30303/udp

WORKDIR /opt/parity

ENTRYPOINT []
CMD ["/opt/parity/start.sh"]
