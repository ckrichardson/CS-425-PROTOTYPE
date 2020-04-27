FROM ubuntu:18.04

USER root
WORKDIR /root

COPY requirements.txt .
COPY wheelhouse .

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    build-essential \
    python3 \
    python3-pip \
    python-pip \
    git \
    curl \
    iproute2 \
    iputils-ping \
    net-tools \
    openvswitch-switch \
    openvswitch-common \
    tcpdump \
    vim \
    x11-xserver-utils \
    xterm \
    libcapstone3 \
    python-dev \
    libffi-dev \ 
    build-essential \ 
    graphviz \ 
    libgraphviz-dev \
    graphviz-dev \ 
    pkg-config \
 && rm -rf /var/lib/apt/lists/*
 
RUN pip3 install atlastk setuptools matplotlib execnet

RUN pip3 install scapy

RUN pip install --no-index --find-links=wheelhouse -r requirements.txt

RUN git clone https://github.com/mininet/mininet.git 

RUN apt update && export PYTHON=/usr/bin/python3 && \
    mininet/util/install.sh -a &&\
    export PYTHONPATH=$PYTHONPATH:/root/mininet

RUN git clone https://gitlab.com/akihe/blab

WORKDIR /root/blab

RUN make && make install
 
WORKDIR /root

RUN git clone https://gitlab.com/akihe/radamsa

WORKDIR /root/radamsa

RUN make && make install

WORKDIR /root

RUN git clone https://github.com/radare/radare2.git

RUN cd radare2 && ./sys/install.sh

WORKDIR /root/radare2/sys
CMD [./install.sh]

RUN echo "Nonce"

RUN git clone -b scapy-testing https://github.com/ckrichardson/CS-425-PROTOTYPE.git CS-425-PROTOTYPE

WORKDIR /root/CS-425-PROTOTYPE

COPY ENTRYPOINT.sh /

RUN chmod +x /ENTRYPOINT.sh

ENTRYPOINT ["/ENTRYPOINT.sh"]

EXPOSE 6633 6653 6640

