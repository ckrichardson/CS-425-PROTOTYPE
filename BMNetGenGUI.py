##############################################################################
# Name: Justin A. Haghighi
# Date: 2020-04-08
# Course: CS 426.1001
# Instructors: Devrin Lee, MS, and Sergiu Dascalu, PhD
# Team: 30
##############################################################################

from BMNetGen import generateTopo
import threading

def generateNetworkBody():
    # Justin's rough HTML body is below
    body = """
    <br>
        <button id="networkStartButton" data-xdh-onevent="networkStart" {}>
            Generate network
        </button>
        </button>
        <button id="networkBenchButton" data-xdh-onevent="networkBench" {}>
            Network benchmark
        </button></button>
        <button id="showGraphButton" data-xdh-onevent="showGraph" {}>
            Show graph
        </button>
    <br>
    """
    return body

def acNetworkStart(dom):
    generateTopo()

def acNetworkBench(dom):
    pass

def acShowGraph(dom):
    pass

networkCallbacks = {
    "networkStart": acNetworkStart,
    "networkBench": acNetworkBench,
    "showGraphButton": acShowGraph,
}







