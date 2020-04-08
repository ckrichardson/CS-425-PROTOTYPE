##############################################################################
# Name: Justin A. Haghighi
# Date: 2020-04-06
# Course: CS 426.1001
# Instructors: Devrin Lee, MS, and Sergiu Dascalu, PhD
# Team: 30
##############################################################################

# allows for the definition of network objects
from mininet.topo import Topo

# allows for running CLI commands via API
from mininet.net import Mininet

# shorten calls to the Mininet module
net = Mininet()

def generateTopo():
    # generate the network nodes and start Mininet, then try calling it
    
    # create network nodes
    c0 = net.addController()
    h0 = net.addHost('h0')
    s0 = net.addSwitch('s0')
    h1 = net.addHost('h1')

    # create network node links
    net.addLink(h0, s0)
    net.addLink(h1, s0)

    # configure interface IP addresses
    h0.setIP('192.168.1.1', 24)
    h1.setIP('192.168.1.2', 24)

    net.start()
    net.pingAll()
