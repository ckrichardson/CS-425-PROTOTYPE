#import each module
#modules should expose a "generate<module>Body()"" function which returns a string of the html
#modules should also expose a dictionary mapping buttons from their html to code within their module
import atlastk as Atlas
from fuzzerGUI import generateFuzzerBody, fuzzerCallbacks
from BMNetGenGUI import generateNetworkBody, networkCallbacks
from binaryAnalysis.GUI import generateIDAttrBody, IDAttrCallbacks 

# Justin commented below two lines out because he is adding his GUI
#def generateNetworkBody():
#    return ""

# networkCallbacks = {}

#def generateIDAttrBody():
#    return ""

idattrCallbacks = {}

main_page = """
<div align="center">
    Main Tools
    <button data-xdh-onevent="loadNetwork">Network Analysis</button><button data-xdh-onevent="loadFuzzer">Fuzzer</button><button data-xdh-onevent="loadIDAttr">IDAttr</button><br><br>
    {}
</div>"""

def acNetwork(dom):
    dom.setLayout("", main_page.format(generateNetworkBody()))

def acFuzzer(dom):
    dom.setLayout("", main_page.format(generateFuzzerBody()))

def acIDAttr(dom):
    dom.setLayout("", main_page.format(generateIDAttrBody()))

callbacks = {
  "": acNetwork,  # Default to network
  "loadNetwork": acNetwork,
  "loadFuzzer": acFuzzer,
  "loadIDAttr": acIDAttr,
}

for key, val in fuzzerCallbacks.items():
    callbacks[key] = val

for key, val in networkCallbacks.items():
    callbacks[key] = val

for key, val in IDAttrCallbacks.items():
    callbacks[key] = val

Atlas.launch(callbacks)
