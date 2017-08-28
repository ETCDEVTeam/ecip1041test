# Usage:
# docker build -f docker/ubuntu/Dockerfile --tag ethcore/parity:branch_or_tag_name .

FROM ubuntu:14.04
WORKDIR /build

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
RUN git clone https://github.com/paritytech/parity.git && \
        cd parity && \
        cargo build --release --verbose && \
        ls /build/parity/target/release/parity && \
        strip /build/parity/target/release/parity

ADD docker/parity/parity.json /build/parity.json

RUN file /build/parity/target/release/parity \
    --chain /build/parity.json \
    --port 31337 \
    --jsonrpc-port 8555
#   --bootnodes enode://xxx@xxx:xxx


EXPOSE 8080 8555 8180
ENTRYPOINT ["/build/parity/target/release/parity"]
