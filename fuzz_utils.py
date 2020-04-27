"""from scapy.all import *
from pox.core import core
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

import subprocess

switch_ip = ""
last_flow_table = ""

#send packet data to switch
def process(fuzz_val) :
    print(fuzz_val)

#ensure flow table remains unchanged
def verify_state():
    curr_flow = subprocess.check_output("ovs-ofctl dump-flows").std_out
    ret = curr_flow == last_flow_table
    last_flow_table = curr_flow
    return ret

#create an openflow packet
def gen_packet():
    packet = scapy.IP()/scapy.OpenFlow(ofp_type = "OFPT_FLOW_MOD")
    return bytes(packet[OpenFlow].payload)
"""

def process(fuzz_val):
    print(fuzz_val)

def verify_state():
    return True

def gen_packet():
    return "A packet"

def openflowPacket(seed):
    return None

def initializeConnection(ip_addr, dport):
    return None


"""
OpenFlow packet grammar
p = match cookie command idle_timeout hard_timeout priority buffer_id out_port flags actions
match = byte byte byte byte
cookie = byte byte byte byte byte byte byte byte
command = 0 0 | 0 1 | 0 2 | 0 3 | 0 4 | byte byte
idle_timeout = byte
hard_timeout = byte
priority = byte
buffer_id = byte byte byte btye
out_port = byte byte
flags = 0 1 | 0 2 | 0 3 | byte byte
byte = [0-15][0-15]
"""
