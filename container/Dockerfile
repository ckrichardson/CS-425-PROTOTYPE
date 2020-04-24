FROM ubuntu:18.04

USER root
WORKDIR /root

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    python3 \
    python3-pip \
    git \
    curl \
    iproute2 \
    iputils-ping \
    mininet \
    net-tools \
    openvswitch-switch \
    openvswitch-testcontroller \
    tcpdump \
    vim \
    x11-xserver-utils \
    xterm \
 && rm -rf /var/lib/apt/lists/* 
 
 RUN pip3 install atlastk
 
 RUN git clone https://github.com/mininet/mininet.git
 
 RUN git clone https://gitlab.com/akihe/blab 
 
 RUN git clone https://gitlab.com/akihe/radamsa 
 
 RUN mininet/util/install.sh
 
EXPOSE 6633 6653 6640

