import os
import sys
import subprocess
import time

# fuzz_me is acting in place of OpenFlow at the miment for packet generation inegration
import fuzz_me
"""
fuzz_me is a placeholder for the module that will construct an openflow
packet from the provided fuzz, send it to the target SDN device on the
mininet network, then use ovs_ofctl to check if the state of the switch
has changed. If the state has changed it will crash in order to trigger
fuzzer success.

That whole thing needs to be initialized separately before EnsembleFuzzer
"""

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

def initRadamsa(ensemble_fuzzer_obj):
    def fuzz(fuzz_obj):
        # this may need to repeat for each type of openflow packet
        packet = fuzz_me.gen_packet()  # radamsa needs an input to mutate
        fuzz_val = subprocess.run("echo {} | radamsa -s {}".format(
            packet, fuzz_obj.seed), shell=True, stdout=subprocess.PIPE).stdout
        fuzz_me.process(fuzz_val)
        return (fuzz_val, fuzz_me.verify_state())

    ensemble_fuzzer_obj.fuzzers.append(
        Fuzzer.fuzzer("radamsa", ensemble_fuzzer_obj.seed, fuzz))


def initBlab(ensemble_fuzzer_obj):
    def fuzz(fuzz_obj):
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
        packet = subprocess.run("blab -s {} -e {}".format(fuzz_obj.seed,
                                                          packet_grammar), shell=True, stdout=subprocess.PIPE).stdout
        packet = packet + action
        fuzz_me.process(packet)
        return (packet, fuzz_me.verify_state())

    ensemble_fuzzer_obj.fuzzers.append(Fuzzer.fuzzer("blab", ensemble_fuzzer_obj.seed, fuzz))

class Fuzzer:

    engines = {
        "radamsa": initRadamsa,
        "blab": initBlab
        }

    class fuzzer:

        def __init__(self, name, seed, fuzz_method):
            self.name = name
            self.seed = seed
            self.fuzz_method = fuzz_method
            # call provided initialize function

        def updateSeed(self, seed):
            self.seed = seed

    def __init__(self, engines, seed):
        self.seed = seed
        self.fuzzers = []
        for e in engines:
            try:
                Fuzzer.engines[e](self)
            except:
                print("Invalid engine: " + e)

    def UpdateSeed(self, val=None):  # should def update this to be a bit more interesting, just sayin'
        if val is not None:
            self.seed = val
        else:
            #hash, append all integers modulo max int?
            self.seed = (4 * self.seed + 3) % 3030303
            for f in self.fuzzers:
                f.seed = self.seed

    def Fuzz(self):
        states = {}
        states["seed"] = self.seed
        for f in self.fuzzers:
            states[f.name] = f.fuzz_method(f)
        self.UpdateSeed()
        # report fuzzer success (to a log file preferably)
        return states
        

    def FuzzTimed(self, fuzz_time):  # fuzz_time is in seconds
        start = time.time()
        while time.time() - start < fuzz_time:
            self.Fuzz()

