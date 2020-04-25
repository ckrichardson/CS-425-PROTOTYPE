import pytest
from EnsembleFuzzer import Fuzzer
from scapy.all import *

#Test reproduceability
def test_reproduceable_fuzz():
    fuzzR1 = Fuzzer(["radamsa"], 1)
    fuzzR2 = Fuzzer(["radamsa"], 1)
    fuzzB1 = Fuzzer(["blab"], 42)
    fuzzB2 = Fuzzer(["blab"], 42)

    success = True

    for i in range(0, 20):
        states = fuzzR1.Fuzz()
        packetR1, garbageVal = states["radamsa"]
        states = fuzzR2.Fuzz()
        packetR2, garbageVal = states["radamsa"]
        assert packetR1 == packetR2
        if packetR1 != packetR2:
            success = False
            print("Radamsa fuzzer failed reproduceability test!")

        states = fuzzB1.Fuzz()
        packetB1, garbageVal = states["blab"]
        states = fuzzB2.Fuzz()
        packetB2, garbageVal = states["blab"]
        assert packetB1 == packetB2
        if packetB1 != packetB2:
            success = False
            print("Blab fuzzer failed reproduceability test!")

        if success == False:
            break

    return success

#Test packet structure
def test_openflow_packet_structure():
    pass

def test_tcp_packet_structure():
    pass

if __name__ == "__main__":
    test_reproduceable_fuzz()
    test_openflow_packet_structure()
    test_tcp_packet_structure()
