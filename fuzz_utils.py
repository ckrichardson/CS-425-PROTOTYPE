from scapy.all import *
from scapy.contrib.openflow import _ofp_header
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.node import Switch
from mininet.clean import Cleanup
from mininet.nodelib import NAT
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.util import irange

import BMNetGen

import subprocess
import random

DEBUG = True

#rflow table (all active host + switch state)
PREV_STATE = ""

def process(packet):
    sendp(packet, verbose= 0 if DEBUG != True else 1)
    if DEBUG:
        packet.show()

def get_current_state():
    state = ""
    if BMNetGen.topo is not None:
        for key, val in BMNetGen.topo.items():
            if isinstance(val, Switch):
                cmd = "ovs-ofctl dump-flows {}".format(key)
                state = state + subprocess.run(cmd, shell=True, 
                        stdout=subprocess.PIPE).stdout.decode("utf8")

    return state


def verify_state():
    current_state = get_current_state()
    global PREV_STATE
    if current_state == PREV_STATE:
        PREV_STATE = current_state
        return True
    else:
        PREV_STATE = current_state
        return False

#returns an OFPTHello packet
def openflowPacket():
    return OFPTHello()

#detect source ip then initiate TCP handshake with target
#if an error occurs, return best possible packet
def initializeConnection(ip_addr, dport):
    #i also need to make sure the last state is known before anything happens >.>
    global PREV_STATE
    if PREV_STATE == "":
        PREV_STATE = get_current_state()

    ip_addr_command = """
    ifconfig | \
    grep -A 1 eth0 | \
    grep -oE 'inet ([[:digit:]]{1,3}\\.){1,3}[[:digit:]]{1,3}' | \
    grep -oE '([[:digit:]]{1,3}\\.){1,3}[[:digit:]]{1,3}'        
    """
    src = subprocess.run(ip_addr_command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')[0:-1]
    if DEBUG:
        print("src_ip: {}".format(src))
    packet = IP(dst=ip_addr, src=src)/TCP(dport=dport)
    packet[TCP].flags = "S"
    packet[TCP].seq = random.randint(0, 2**32)
    response = sr1(packet, timeout=0.125, verbose=0)
    if response is None:
        return packet

    packet[TCP].flags = "A"
    packet[TCP].ack = response[TCP].seq + 1
    packet[TCP].seq = packet.seq + 1
    packet.show()
    response = sr1(packet, timeout=0.125, verbose=0)
    if response is None:
        packet[TCP].seq = packet[TCP].seq + 1
        packet[TCP].flags = ""
        return packet

    packet[TCP].ack = response[TCP].seq + 1
    packet[TCP].seq = packet[TCP].seq + 1
    packet[TCP].flags = ""

    return packet

