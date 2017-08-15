FROM debian:stretch

RUN apt-get update && \
    apt-get -y install wget unzip git && \
    apt-get -y install cmake build-essential g++ libboost-all-dev && \
    apt-get -y install libleveldb-dev libmicrohttpd-dev libjsonrpccpp-dev libjsonrpccpp-tools opencl-headers && \
    apt-get -y install libcrypto++-dev libminiupnpc-dev libgmp-dev

RUN cd /opt && \
    git clone --recursive https://github.com/ethereum/cpp-ethereum.git && \
    cd /opt/cpp-ethereum && \
    git checkout 646738ca && \
    mkdir build && \
    cd build && \
    cmake .. -DEVMJIT=OFF -DTESTS=OFF -DETHASHCL=OFF -DSOLIDITY=OFF && \
    cmake --build . && \
    cd /opt/cpp-ethereum && \
    mkdir -p /opt/ethminer && \
    cd /opt/cpp-ethereum/build && \
    cp ./ethminer/ethminer /opt/ethminer/ && \
    cp ./libdevcrypto/libdevcrypto.so /opt/ethminer/ && \
    cp ./libdevcore/libdevcore.so /opt/ethminer/ && \
    cp ./libethcore/libethcore.so /opt/ethminer/ && \
    cp ./libethereum/libethereum.so /opt/ethminer/ && \
    cp ./libethashseal/libethashseal.so /opt/ethminer/ && \
    cp ./libethash/libethash.so /opt/ethminer/ && \
    cp ./libevm/libevm.so /opt/ethminer/ && \
    cp ./libevmcore/libevmcore.so /opt/ethminer/ && \
    cp ./libp2p/libp2p.so /opt/ethminer/ && \
    cp ./utils/libscrypt/libscrypt.so /opt/ethminer/ && \
    cd / && \
    rm -rf /opt/cpp-ethereum

WORKDIR /opt/ethminer

CMD /opt/ethminer/ethminer --cpu -t 1 --farm-recheck 10000

