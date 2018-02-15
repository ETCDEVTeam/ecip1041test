FROM ubuntu

# prepare patch that changes exponential difficulty growth period from 100000 to 100 blocks
COPY docker/parity/001-Reduce-EXP_DIFF_PERIOD-to-100.patch /opt/parity/

ENV PATH /root/.cargo/bin:$PATH
ENV RUST_BACKTRACE 1
WORKDIR /build


RUN apt-get update && \
    apt-get -y install wget unzip jq dnsutils netcat vim git && \
    apt-get -y install g++ build-essential curl git file binutils libssl-dev pkg-config libudev-dev && \
    apt-get -y install python python-pip python-setuptools python-dev && \
    pip install ecdsa && \
    pip install pysha3 && \
    wget -O toxiproxy-2.1.2.deb --progress=dot:mega https://github.com/Shopify/toxiproxy/releases/download/v2.1.2/toxiproxy_2.1.2_amd64.deb && \
    dpkg -i toxiproxy-2.1.2.deb && \
    rm toxiproxy-2.1.2.deb && \
    # fetch and patch parity
	git clone https://github.com/paritytech/parity.git && \
	cd parity && \
    git checkout v1.9.2 && \
    git apply /opt/parity/001-Reduce-EXP_DIFF_PERIOD-to-100.patch && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    cargo build --release --verbose && \
    strip /build/parity/target/release/parity && \
    file /build/parity/target/release/parity && \
    mkdir -p /opt/parity/ && \
    cp /build/parity/target/release/parity /opt/parity/ && \
	rm -rf /root/.cargo /root/.multirust /root/.rustup /build && \
    apt-get purge -y  \
        # make
        build-essential \
        # add-apt-repository
        software-properties-common \
        make \
        curl \
        wget \
        git \
        g++ \
        gcc \
        binutils \
        file \
        pkg-config \
        dpkg-dev \
        # evmjit dependencies
        zlib1g-dev \
        libedit-dev \
        cmake llvm-3.7-dev &&\
    rm -rf /var/lib/apt/lists/*

COPY docker/parity/start.sh /opt/parity/start.sh
COPY docker/parity/ecip1041chain.json /opt/parity/ecip1041chain.json
COPY bin/ids.py /opt/parity/

RUN chmod +x /opt/parity/start.sh

EXPOSE 8545
EXPOSE 30303
EXPOSE 30303/udp
EXPOSE 40404

WORKDIR /opt/parity

ENTRYPOINT []
CMD ["/opt/parity/start.sh"]
