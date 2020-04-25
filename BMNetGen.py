###############################################################################
# Name: Justin A. Haghighi
# Date: 2020-04-06
# Course: CS 426.1001
# Instructors: Devrin Lee, MS, and Sergiu Dascalu, PhD
# Team: 30
###############################################################################

###############################################################################
# Import Mininet tools
###############################################################################
# allows for the definition of network objects
from mininet.topo import Topo

# allows for running CLI commands via API
from mininet.net import Mininet

# allows for node connection parameters to be printed
from mininet.util import dumpNodeConnections

# allows for CPU limits
from mininet.node import CPULimitedHost

# allows for cleanup of mininet
from mininet.clean import Cleanup

###############################################################################
# Import plotting tools
###############################################################################
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

import re

# defines the network topology
class BMTopo(Topo):

    # The topology is hard coded here
    def build(self):

        # Add hosts
        h0 = self.addHost('h0')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Add switches
        s0 = self.addSwitch('s0')

        # Add links
        self.addLink(h0, s0)    
        self.addLink(h1, s0)
        self.addLink(h2, s0)

# generates a simpler topo
def generateTopo():
    # generate the network nodes and start Mininet
    
    net = Mininet()

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
    net.stop()

# runs an iperf test between hosts in the topology
def bandwidthTest():
    # create network topology
    topo = BMTopo()
    
    # configure Mininet
    net = Mininet(topo=topo, host=CPULimitedHost)

    # dump node connections
    print("\n*** Dumping node connections\n")
    dumpNodeConnections(net.hosts)

    net.start()

    # test connectivity
    print("\n*** Ping test for all hosts\n")
    net.pingAll()

    # test bandwidth with iperf
    perfList = [] # list stores result of bandwidth test

    print("\n*** Test bandwidth between h0 and h1\n")
    h1, h2 = net.get('h0', 'h1')
    perfList = net.iperf((h1, h2))

    # stop the Mininet network
    print("\n*** Stop network")
    net.stop()
    
    return perfList

# plot the network
def plotNet():
    # get the data to plot   
    hostBandwidth = bandwidthTest()

    # process hostBandwidth to extract numerical values only
    # strips the unit from each list element
    hostBandwidthNumerals = []

    for element in hostBandwidth:
        temp = re.findall(r'\d+.\d', element)
        hostBandwidthNumerals.append(temp)

    # each numeral is in its own list in hostBandwidthNumerals
    # flatten the list using list comprehension
    hostBandwidthNumeralsFlat = [y for x in hostBandwidthNumerals for y in x]

    # hostBandwidthNumeralsFlat is a list of strings
    # convert the strings to int using list comprehension
    hostBandwidthNumeralsFlat = [float(f) for f in hostBandwidthNumeralsFlat]

    # hosts to plot
    plotHosts = ('Host 1', 'Host 2')
    y_pos = np.arange(len(plotHosts))
    
    plt.bar(y_pos, hostBandwidthNumeralsFlat, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, plotHosts)
    plt.ylabel('Average Tput in Gbits/sec')
    plt.title('SDN Host Bandwidth')

    plt.show()


    

    
    
