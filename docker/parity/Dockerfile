FROM ubuntu

RUN apt-get update && \
    apt-get -y install wget unzip jq dnsutils netcat vim git

RUN apt-get -y install python python-pip python-setuptools python-dev && \
    pip install ecdsa && \
    pip install pysha3

RUN wget -O toxiproxy-2.1.2.deb --progress=dot:mega https://github.com/Shopify/toxiproxy/releases/download/v2.1.2/toxiproxy_2.1.2_amd64.deb && \
    dpkg -i toxiproxy-2.1.2.deb && \
    rm toxiproxy-2.1.2.deb

# prepare patch that changes exponential difficulty growth period from 100000 to 100 blocks
COPY docker/parity/001-Reduce-EXP_DIFF_PERIOD-to-100.patch /tmp/

# get parity v1.9.2 sources and apply patch
WORKDIR /build
RUN git clone https://github.com/paritytech/parity.git && \
	cd parity && \
    git checkout v1.9.2 && \
    git apply /tmp/001-Reduce-EXP_DIFF_PERIOD-to-100.patch



# from parity's Dockerfile

# install tools and dependencies
RUN apt-get update && \
        apt-get install -y \
        g++ \
        build-essential \
        curl \
        git \
        file \
        binutils \
        libssl-dev \
        pkg-config \
        libudev-dev

# install rustup
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# rustup directory
ENV PATH /root/.cargo/bin:$PATH

# show backtraces
ENV RUST_BACKTRACE 1

# show tools
RUN rustc -vV && \
cargo -V && \
gcc -v &&\
g++ -v

# build parity
ADD . build/parity
RUN cd parity && \
        cargo build --release --verbose && \
        ls /build/parity/target/release/parity && \
        strip /build/parity/target/release/parity

RUN file /build/parity/target/release/parity

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
