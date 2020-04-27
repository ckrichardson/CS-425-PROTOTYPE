from scapy.all import *
from scapy.contrib.openflow import _ofp_header
from scapy.fields import ByteEnumField, IntEnumField, IntField, LongField, PacketField, ShortField, XShortField
from scapy.layers.l2 import Ether
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

import subprocess
import random

DEBUG = True

PREV_STATE = ""

def process(packet):
    send(packet)
    if DEBUG:
        print("Displaying packet...")
        packet.display()

def verify_state():
    return True

#returns an OFPTHello packet
def openflowPacket():
    return IP()/TCP()/OFPTHello()

#detect source ip then initiate TCP handshake with target
#if an error occurs, return best possible packet
def initializeConnection(ip_addr, dport):
    ip_addr_command = """
    ifconfig | \
    grep -A 1 eth0 | \
    grep -oE "inet \([[:digit:]]{1,3}\\\\.\){3}[[:digit:]]{1,3} | \
    grep -oE "\([[:digit:]]{1,3}\\\\.\){3}[[:digit:]]{1,3}        
    """
    src = subprocess.run(ip_addr_command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print("SRC_ip is {}".format(src));
    packet = IP(dst=ip_addr, src=src)/TCP(dport=dport)
    packet[TCP].flags = "S"
    packet[TCP].seq = random.randint(0, 2**32)
    response = sr1(packet, timeout=0.125, verbose=0)
    if response is None:
        print("returning emergency packet, as i should")
        return packet

    packet[TCP].flags = "A"
    packet[TCP].ack = response[TCP].seq + 1
    packet[TCP].seq = packet.seq + 1
    response = sr1(packet, timeout=0.125, verbose=0)
    if response is None:
        packet[TCP].seq = packet[TCP].seq + 1
        packet[TCP].flags = ""
        return packet

    packet[TCP].ack = response[TCP].seq + 1
    packet[TCP].seq = packet[TCP].seq + 1
    packet[TCP].flags = ""

    return packet

