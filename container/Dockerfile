FROM ubuntu:18.04

USER root
WORKDIR /root

COPY ENTRYPOINT.sh /

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    python3 \
    python3-pip \
    git \
    curl \
    iproute2 \
    iputils-ping \
    net-tools \
    openvswitch-switch \
    openvswitch-testcontroller \
    tcpdump \
    vim \
    x11-xserver-utils \
    xterm \
 && rm -rf /var/lib/apt/lists/* \
 && chmod +x /ENTRYPOINT.sh
 
RUN pip3 install atlastk setuptools

RUN pip3 install scapy
 
RUN git clone https://github.com/mininet/mininet.git 

RUN apt update && export PYTHON=/usr/bin/python3 && \
    mininet/util/install.sh && apt install -y mininet &&\
    export PYTHONPATH=$PYTHONPATH:/root/mininet

RUN git clone https://gitlab.com/akihe/blab 

WORKDIR /root/blab

RUN make && make install
 
WORKDIR /root

RUN git clone https://gitlab.com/akihe/radamsa 

WORKDIR /root/radamsa

RUN make && make install

WORKDIR /root

RUN git clone https://github.com/ckrichardson/CS-425-PROTOTYPE

WORKDIR /root/CS-425-PROTOTYPE

ENTRYPOINT ["/ENTRYPOINT.sh"]

EXPOSE 6633 6653 6640

