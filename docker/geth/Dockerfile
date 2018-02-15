FROM ubuntu

ENV PATH /root/.cargo/bin:/opt/go/bin:$PATH
ENV GOROOT /opt/go
ENV GOPATH /root/go

COPY docker/geth/0001-Reduce-ExpDiffPeriod-to-100.patch /opt/geth/

RUN apt-get update && \
    apt-get -y install wget unzip git jq dnsutils netcat vim git curl && \
    apt-get -y install python-pip python-setuptools python-dev && \
    pip install ecdsa && \
    pip install pysha3 && \
    wget -O toxiproxy-2.1.2.deb --progress=dot:mega https://github.com/Shopify/toxiproxy/releases/download/v2.1.2/toxiproxy_2.1.2_amd64.deb && \
    dpkg -i toxiproxy-2.1.2.deb && \
    rm toxiproxy-2.1.2.deb && \
	# install rust
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
	# install go
	cd opt && \
	wget --progress=dot:mega https://dl.google.com/go/go1.9.4.linux-amd64.tar.gz && \
    tar xzf go1.9.4.linux-amd64.tar.gz && rm go1.9.4.linux-amd64.tar.gz && \
   	go env && \
	# build geth with SputnikVM
    git clone https://github.com/ethereumproject/sputnikvm-ffi $GOPATH/src/github.com/ethereumproject/sputnikvm-ffi && \
    cd $GOPATH/src/github.com/ethereumproject/sputnikvm-ffi/c/ffi && cargo build --release && \
    cp $GOPATH/src/github.com/ethereumproject/sputnikvm-ffi/c/ffi/target/release/libsputnikvm_ffi.a $GOPATH/src/github.com/ethereumproject/sputnikvm-ffi/c/libsputnikvm.a && \
	go get -d github.com/ethereumproject/go-ethereum/... && \
    cd $GOPATH/src/github.com/ethereumproject/go-ethereum && \
	git checkout defused-enabled && \
    git apply /opt/geth/0001-Reduce-ExpDiffPeriod-to-100.patch && \
    export CGO_LDFLAGS="$GOPATH/src/github.com/ethereumproject/sputnikvm-ffi/c/libsputnikvm.a -ldl" && \
    export EXT_LD_FLAGS="-extldflags=-static" && \
    # go install ... doesn't work with netgo on CircleCI on Linux
    go build -tags="sputnikvm netgo" -ldflags "$EXT_LD_FLAGS -X main.Version=`git describe --tags`" ./cmd/geth && \
    mv geth /opt/geth/ && \
	cd && \
	rm -rf /root/.cargo /root/.multirust /root/.rustup /build $GOPATH && \
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
