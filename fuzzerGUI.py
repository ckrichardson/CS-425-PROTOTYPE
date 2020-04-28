from EnsembleFuzzer import Fuzzer
import BMNetGen 
import threading
import time

enableCancel = False
enableStart = True

fuzzingStatus = ""
targetSelection = "Please Select"
selectedFuzzers = []
for fuzz in Fuzzer.engines.keys():
    selectedFuzzers.append(fuzz)
fuzzTimeText = "60"
fuzzSeedText = "0"

def generateFuzzerBody():
    target_options = ""
    if BMNetGen.topo is not None:
        for node, val in BMNetGen.topo.items():
            if val.IP() != "127.0.0.1":
                target_options = target_options + "\n<option value=\"{}\">{}</option>".format(val.IP(), node + ": " + val.IP())
        target_options = target_options + "\n<option value=\"{}\">{}</option>".format("127.0.0.1", "switch")

    engine_options = ""
    for fuzz in Fuzzer.engines.keys():
        selected = ""
        if fuzz in selectedFuzzers:
            selected = "checked"
        engine_options = engine_options + "\n<input type=\"checkbox\" id=\"{}\" {}>\n".format(fuzz, selected)
        engine_options = engine_options + "<label for=\"{}\">{}</label><br>".format(fuzz, fuzz.capitalize())

    global enableStart
    global enableCancel

    cancelEnabled = ""
    if not enableCancel:
        cancelEnabled = "disabled"

    startEnabled = ""
    if not enableStart:
        startEnabled = "disabled"

    body = """
    <div align="center">
        <div align="center">
            <div align="left" style="display: inline-block">
                <form>
                    <label for="ip">Select fuzzer target</label><br>
                    <select id="ip">
                    <option value="" selected disabled hidden>{}</option>
                    {}
                    </select>
                </form>
                <br>
            </div>
            <div align="left" style="display: inline-block">
                <form>
                    <label for="seed">Set Seed</label><br>
                    <input type="number" step="1" min="0" id="seed" name="seed" value="{}" style="width:100px">
                </form>
                <br>
            </div>
        </div>
        <div align="left" style="display: inline-block">
            <label for="checkme">Select Fuzzers</label>
            <form id="checkme">
            {}
            </form>
            <br>
        </div>
        <div>
            <form>
                <label for="time">Set fuzzing time constraint</label><br>
                <input type="number" step="0.001" min="0" id="time" name="time" value="{}" style="width:100px">
            </form>
            <br>
        </div>
        <button id="fuzzStartButton" data-xdh-onevent="startFuzzer" {}>
        Begin
        </button>
        <button id="fuzzCancelButton" data-xdh-onevent="endFuzzer" {}>
            Cancel
        </button>
        <br>
        <p id="fuzzStatus">{}</p>
    </div>
    """.format(targetSelection, target_options, fuzzSeedText, 
                engine_options, fuzzTimeText, startEnabled, 
                cancelEnabled, fuzzingStatus)
    return body

fuzz_thread = None
keep_fuzzing = True

def acCancelFuzzer(dom):
    global keep_fuzzing
    global fuzz_thread
    keep_fuzzing = False
    if fuzz_thread is not None:
        fuzz_thread.join()
    fuzz_thread = None
    
def fuzz_thread_func(dom, target, seed, fuzztime, fuzzers):
    successful_seeds = ""
    dom.enableElement("fuzzCancelButton")
    dom.disableElement("fuzzStartButton")
    global enableCancel
    global enableStart
    global fuzzingStatus
    enableCancel = True
    enableStart = False
    fuzzingStatus = "Fuzzing target: {}".format(target)
    dom.setContent("fuzzStatus", fuzzingStatus)
    fuzzer = Fuzzer(fuzzers, seed)
    start = time.time()
    global keep_fuzzing
    keep_fuzzing = True
    while time.time() - start < fuzztime:
        if keep_fuzzing == False:
            break
        try:
            success = fuzzer.Fuzz()
            if success != None:
                seed_out, states = success
                print(str(seed_out) + ": " + str(states))
                successful_seeds = successful_seeds + "\n" + str(seed_out)
                fuzzingStatus = "Fuzzing target: {}".format(target + successful_seeds)
                dom.setContent("fuzzStatus", fuzzingStatus)
        except:
            continue
    fuzzingStatus = "Finished fuzzing {}".format(target + successful_seeds)
    print(fuzzingStatus)
    dom.setContent("fuzzStatus", fuzzingStatus)
    dom.disableElement("fuzzCancelButton")
    dom.enableElement("fuzzStartButton")
    keep_fuzzing = True
    enableCancel = False
    enableStart = True

def acStartFuzzer(dom):
    if fuzz_thread is not None:
        return
    global targetSelection
    targetSelection = dom.getContent("ip")
    if targetSelection == "":
        print("Invalid selection")
        dom.setContent("fuzzStatus", "Please select a target from the drop down menu.\nBe sure to generate a network first!")
        return
    Fuzzer.TARGET = targetSelection
    if Fuzzer.TARGET == "127.0.0.1":
        Fuzzer.TARGET_TYPE = "switch"
    else:
        Fuzzer.TARGET_TYPE = "machine"
    print("Fuzzing target: {}".format(targetSelection))
    global fuzzSeedText 
    fuzzSeedText = dom.getContent("seed")
    if fuzzSeedText == "":
        fuzzSeedText = "0"
    dom.setContent("seed", fuzzSeedText)
    seed = abs(int(fuzzSeedText, 10))
    global fuzzTimeText
    fuzzTimeText = dom.getContent("time")
    if fuzzTimeText == "":
        fuzztime = 60 * 60 * 24 * 5 #five days should be indefinite enough
    else:
        try:
            fuzztime = abs(float(fuzzTimeText))
        except:
            fuzztime = 60 * 60 * 24 * 5 #why u gotta break it?
    fuzzTimeText = str(fuzztime)
    dom.setContent("time", fuzzTimeText)
    global selectedFuzzers
    selectedFuzzers = []
    for engine in Fuzzer.engines.keys():
        if dom.getContent(engine) == "true":
            selectedFuzzers.append(engine)
    global fuzz_thread
    fuzz_thread = threading.Thread(target=fuzz_thread_func, args=(dom, targetSelection, seed, fuzztime, selectedFuzzers))
    fuzz_thread.start()

fuzzerCallbacks = {
  "startFuzzer": acStartFuzzer,
  "endFuzzer": acCancelFuzzer,
}
