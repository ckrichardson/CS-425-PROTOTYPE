from EnsembleFuzzer import Fuzzer

#Test reproduceability
def reproduceabilityTest():
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
        if packetR1 != packetR2:
            success = False
            print("Radamsa fuzzer failed reproduceability test!")
    
        states = fuzzB1.Fuzz()
        packetB1, garbageVal = states["blab"]
        states = fuzzB2.Fuzz()
        packetB2, garbageVal = states["blab"]
        if packetB1 != packetB2:
            success = False
            print("Blab fuzzer failed reproduceability test!")
        
        if success == False:
            break

    return success

#Test packet structure

if __name__ == "__main__":
    reproduceabilityTest()