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
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.clean import Cleanup
from mininet.nodelib import NAT
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.util import irange

###############################################################################
# Import plotting tools
###############################################################################
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

# use a noninteractive backend for matplotlib
matplotlib.use('Agg')

# import regular expression library for list processing
import re

# import base64 to process the tput graph and reveal in Atlas
import base64

topo = None

# defines the network topology
class BMTopo(Topo):
    
    # the topology is hard coded here
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

# defines a NAT topology
class BMNatTopo(Topo):

    # the topology is described here
    # it consists of numNATHosts
    def build(self, numNATHosts = 2, **_kwargs):
        # add external switch
        externalSwitch = self.addSwitch('s0')
        # add external host
        externalHost = self.addHost('h0')
        # link the external devices together
        self.addLink(externalSwitch, externalHost)
        
        # create the private NAT networks
        for numNATNets in irange(1, numNATHosts):
            externalInterface = 'nat%d-eth0' % numNATNets
            privateInterface = 'nat%d-eth1' % numNATNets
            privateIP = '192.168.%d.1' % numNATNets
            privateSubnet = '192.168.%d.0/24' % numNATNets
            parameters = {'ip': '%s/24' % privateIP}
        
        # add NAT to topo
        nat = self.addNode('nat%d' % numNATNets, cls = NAT,
                           subnet = privateSubnet, 
                           inetIntf = externalInterface, 
                           localIntf = privateInterface)
        nSwitch = self.addSwitch('s%d' % numNATNets)
        
        # connect private and external nets
        self.addLink(nat, externalSwitch, intfName1 = externalInterface)
        self.addLink(nat, nSwitch, ilntfName1 = privateInterface, 
                     params1 = parameters)
        
        # add host and connect to private switch
        nHost = self.addHost('h%d' % numNATNets, 
                            ip = '192.168.%d.100/24' % numNATNets,
                            defaultRoute = 'via %s' % privateIP)
        self.addLink(nHost, nSwitch)        
        
# generates a simpler topo
def generateTopo():
    # generate the network nodes and start Mininet
    
    net = Mininet()

    # create network nodes
    c0 = net.addController()
    h0 = net.addHost('h0')
    h0 = net.get('h0')
    s0 = net.addSwitch('s0')
    h1 = net.addHost('h1')
    h1 = net.get('h1')

    # create network node links
    net.addLink(h0, s0)
    net.addLink(h1, s0)

    # configure interface IP addresses
    h0.setIP('192.168.1.1', 24)
    h1.setIP('192.168.1.2', 24)

    net.start()
    net.pingAll()
    global topo
    topo = net

def stopTopo():
    Mininet.stop(self)

def generateNATTopo():
    
    global topo

    # generates a NAT topo
    topo = BMNatTopo()
    net = Mininet(topo=topo)

    # dump node connections
    print("\n*** Dumping node connections\n")
    dumpNodeConnections(net.hosts)

    net.start()

    # test connectivity
    print("\n*** Ping test for all hosts\n")
    net.pingAll()
    
    # stop network
    net.stop()
    
# runs an iperf test between hosts in the topology
def bandwidthTest():

    global topo
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
# returns the graph encoded as base64 for frontend
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

    # configure the bar graph
    plotHosts = ('Host 1', 'Host 2')
    y_pos = np.arange(len(plotHosts))
    
    plt.bar(y_pos, hostBandwidthNumeralsFlat, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, plotHosts)
    plt.ylabel('Average Tput in Gbits/sec')
    plt.title('SDN Host Bandwidth')

    # save the bar graph
    plt.plot(hostBandwidthNumeralsFlat)
    plt.savefig('tput_graph.png')

    # convert PNG to base64
    with open('tput_graph.png', 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read())
    print(base64_image.decode('utf-8'))            

    
    
