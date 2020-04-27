import os
import sys
import subprocess
import time
from datetime import date
import random
from scapy.all import *
from scapy.contrib.openflow import *

# fuzz_utils interfaces with the mininet network and openflow vswitch
import fuzz_utils

#radamsa and blab both support arbitrarily large positive integers, 
#so set this to whatever you like
#obvs this will affect reproduceability
MAX_SEED_INT = 9223372036854775807

#initialization functions for individual fuzzers
#to add another fuzzer X create an init<X>(ensemble_fuzzer_obj) function
#which does the following:
#   define a fuzz(fuzz_obj) function that provides fuzzing instructions
#       -generate a packet
#       -send the packet
#       -return state verification
#   end of function should be:
#       ensemble_fuzzer_obj.fuzzers.append(Fuzzer.fuzzer(<name>, ensemble_fuzzer_obj.seed, fuzz))
#then, inside the fuzzer class, add the mapping <name>: init<X> to the engines dictionary

#radamsa helper function to generate a standard TCP packet 
def radamsa_host_packet():
    packet = fuzz_utils.initializeConnection(Fuzzer.TARGET, 430)
    packet_payload = subprocess.run("echo {} | radamsa -s {}".format(
                                    Fuzzer.DEFAULT_PACKET_PAYLOAD, fuzz_obj.seed), 
                                    shell=True, stdout=subprocess.PIPE).stdout
    packet.add_payload(packet_payload)
    print(str(packet))
    return str(packet)

#radamsa helper unction to generate a mangled openflow hello packet 
def radamsa_switch_packet():
    packet = fuzz_utils.initializeConnection(Fuzzer.TARGET, 6653)
    valid_openflow = fuzz_utils.openflowPacket().raw()
    packet_payload = subprocess.run("echo {} | radamsa -s {}".format(
                                    valid_openflow, fuzz_obj.seed), 
                                    shell=True, stdout=subprocess.PIPE).stdout
    packet.add_payload(packet_payload)
    return str(packet)

#radamsa initialization function
def initRadamsa(ensemble_fuzzer_obj):
    def fuzz(fuzz_obj):
        # this may need to repeat for each type of openflow packet
        packet = None
        if Fuzzer.TARGET_TYPE == "machine":
            packet = IP(radamsa_host_packet())
        else:
            packet = IP(radamsa_switch_packet())

        fuzz_utils.process(packet)
        return fuzz_utils.verify_state()

    ensemble_fuzzer_obj.fuzzers.append(
        Fuzzer.fuzzer("radamsa", ensemble_fuzzer_obj.seed, fuzz))

#blab helper function for generating
def blab_host_packet():
    tcp_packet_grammar = "'output = P \
        P = sport dport seq ack doffset reserved flags window checksum urget_p options padding data \
        sport = byte byte \
        dport = byte byte \
        seq = byte byte byte byte \
        ack = byte byte byte byte \
        doffset = bit bit bit bit \
        reserved = bit bit bit \
        flags = byte bit \
        window = byte byte \
        checksum = byte byte \
        urgent_p = byte byte \
        options = byte byte byte \
        padding = byte \
        data = byte | data byte \
        bit = 1 | 0 \
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 \
        byte = d d' \
        "
    tcp_payload = subprocess.run("blab -s {} -e {}".format(fuzz_obj.seed,tcp_packet_grammar), 
                                shell=True, stdout=subprocess.PIPE).stdout
    tcp_payload = TCP(tcp_payload)
    packet = fuzz_utils.initializeConnection(Fuzzer.TARGET, 430)
    packet[TCP] = tcp_payload
    return str(packet)

def blab_switch_packet():
    action_grammars = [
        "'output = A\
        A = 0 0 0 8 port max_len\
        port = byte byte\
        max_len = byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 1 0 8 vlan_vid pad\
        vlan_vid = byte byte\
        pad = byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 2 0 8 vlan_pc pad\
        vlan_pc = byte byte\
        pad = byte byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 3 0 4'\
        ",
        "'output = A\
        A = 0 4 0 15 setdlsrc pad\
        setdlsrc = byte byte byte byte byte byte\
        pad = byte byte byte byte byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 5 0 15 setdldst pad\
        setdldst = byte byte byte byte byte byte\
        pad = byte byte byte byte byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 6 0 8 nw_addr\
        nw_addr = byte byte byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 7 0 8 nw_addr\
        nw_addr = byte byte byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 8 0 8 nw_tos pad\
        nt_tos = byte byte\
        pad = byte byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 9 0 8 port pad\
        port = byte byte\
        pad = byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 10 0 8 port pad\
        port = byte byte\
        pad = byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        ",
        "'output = A\
        A = 0 11 0 15 port pad queue_id\
        port = byte byte\
        pad = byte byte byte byte byte byte\
        queue_id = byte byte byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        "
    ]
    action = subprocess.run("blab -s {} -e {}".format(fuzz_obj.seed, action_grammars[fuzz_obj.seed % len(
        action_grammars)]), shell=True, stdout=subprocess.PIPE).stdout
    packet_grammar = "'output = P\
        P = match cookie command idle_timeout hard_timeout priority buffer_id out_port flags\
        match = byte byte byte byte\
        cookie = byte byte byte byte byte byte byte byte\
        command = 0 0 | 0 1 | 0 2 | 0 3 | 0 4 | byte byte\
        idle_timeout = byte\
        hard_timeout = byte\
        priority = byte\
        buffer_id = byte byte byte byte\
        out_port = byte byte\
        flags = 0 1 | 0 2 | 0 3 | byte byte\
        d = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15\
        byte = d d'\
        "  # .format(str("\"".encode() + action[2:-1] + "\"".encode())[2:-1])
    packet = subprocess.run("blab -s {} -e {}".format(fuzz_obj.seed,packet_grammar), 
                            shell=True, stdout=subprocess.PIPE).stdout
    ofp_packet = packet + action
    packet = fuzz_utils.initializeConnection(Fuzzer.TARGET, 6653)/OFPAT(ofp_packet)
    return str(packet)


#blab initialization function
def initBlab(ensemble_fuzzer_obj):
    def fuzz(fuzz_obj):
        packet = None
        if Fuzzer.TARGET_TYPE == "switch":
            packet = IP(blab_switch_packet())
        else:
            packet = IP(blab_host_packet())

        fuzz_utils.process(packet)
        return fuzz_utils.verify_state()

    ensemble_fuzzer_obj.fuzzers.append(Fuzzer.fuzzer("blab", ensemble_fuzzer_obj.seed, fuzz))

class Fuzzer:

    #target can be either machine or switch (tells fuzzers what type of packets to create)
    TARGET_TYPE = "machine"
    TARGET = ""

    DEFAULT_PACKET_PAYLOAD = "A valid packe! :D"

    engines = {
        "radamsa": initRadamsa,
        "blab": initBlab
        }

    class fuzzer:

        def __init__(self, name, seed, fuzz_utilsthod):
            self.name = name
            self.seed = seed
            self.fuzz_utilsthod = fuzz_utilsthod
            # call provided initialize function

        def updateSeed(self, seed):
            self.seed = seed

    def __init__(self, engines, seed):
        self.seed = seed
        self.generator = random.Random(seed)
        self.fuzzers = []
        for e in engines:
            try:
                Fuzzer.engines[e](self)
            except:
                print("Invalid engine: " + e)

    def UpdateSeed(self, val=None): 
        if val is not None:
            self.seed = val
            self.generator = random.Random(self.seed)
        else:
            global MAX_SEED_INT
            self.seed = self.generator.randint(0, MAX_SEED_INT)
        for f in self.fuzzers:
            f.seed = self.seed

    def Fuzz(self):
        states = {}
        for f in self.fuzzers:
            states[f.name] = f.fuzz_utilsthod(f)
        self.UpdateSeed()
        # report fuzzer success (to a log file preferably)
        with open("fuzzer_log_" + date.today().strftime("%d%m%Y") + ".txt", "a+") as log_file:
            log_file.write(Fuzzer.TARGET)
            log_file.write(Fuzzer.TARGET_TYPE)
            log_file.write(states)
        for key, val in states:
            if val is False:
                return (self.seed, states)
        return None
        

    def FuzzTimed(self, fuzz_time):  # fuzz_time is in seconds
        start = time.time()
        while time.time() - start < fuzz_time:
            self.Fuzz()

