from EnsembleFuzzer import Fuzzer
import threading
import time

enableCancel = False
enableStart = True

fuzzingStatus = ""
targetSelection = ""
selectedFuzzers = []
for fuzz in Fuzzer.engines.keys():
    selectedFuzzers.append(fuzz)
fuzzTimeText = "60"
fuzzSeedText = "0"

def generateFuzzerBody():
    topo = ["127.0.0.1", "196.168.4.15", "10.0.0.1"]
    target_options = ""
    for ip in topo:
        target_options = target_options + "\n<option value=\"{}\">{}</option>".format(ip, ip)

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
                    <input type="text" id="seed" name="seed" value="{}" style="width:100px">
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
                <input type="text" id="time" name="time" value="{}" style="width:100px">
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
    """.format(targetSelection, target_options, fuzzSeedText, engine_options, fuzzTimeText, startEnabled, cancelEnabled, fuzzingStatus)
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
    while time.time() - start < fuzztime:
        if keep_fuzzing == False:
            break
        try:
            states = fuzzer.Fuzz()
            for fuzz_name in fuzzers:
                packet, state = states[fuzz_name]
                if state == True:
                    successful_seeds = successful_seeds + "\n{}:{}".format(fuzz_name, str(states["seed"]))
                    fuzzingStatus = "Fuzzing target: {}".format(target + successful_seeds)
                    dom.setContent("fuzzStatus", fuzzingStatus)
        except:
            continue
    fuzzingStatus = "Finished fuzzing {}".format(target + successful_seeds)
    dom.setContent("fuzzStatus", fuzzingStatus)
    dom.disableElement("fuzzCancelButton")
    dom.enableElement("fuzzStartButton")
    keep_fuzzing = True
    enableCancel = False
    enableStart = True

def acStartFuzzer(dom):
    global targetSelection
    targetSelection = dom.getContent("ip")
    print("Fuzzing target: {}".format(targetSelection))
    global fuzzSeedText 
    fuzzSeedText = dom.getContent("seed")
    if fuzzSeedText == "":
        fuzzSeedText = "0"
    dom.setContent("seed", fuzzSeedText)
    seed = int(fuzzSeedText, 10)
    global fuzzTimeText
    fuzzTimeText = dom.getContent("time")
    if fuzzTimeText == "":
        fuzztime = 60 * 60 * 24 * 5 #five days should be indefinite enough
    else:
        fuzztime = float(fuzzTimeText)
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