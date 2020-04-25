from PRG_analysis import *
import importlib
import inspect
import modules.module_analytics
import modules.module_graphbuilder
import time
import pygraphviz as pgv


"""
This is a modularized version of the ICSREF analysis module.
It has been modified such that it can exist separately.

Code courtesy of MoMA labs
"""
def binary_analysis(path, graph):
    prg = Program(path)

    path = os.path.join('results', prg.name)

    # The following ICSREF code was modified for a more modular, non-interactive shell.
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    # determine the output analytics file
    txt_f = open(os.path.join(path, '{}.analytics'.format(prg.name)), 'w')

    totals = {}

    for fun in prg.Functions:
        # Find subroutine signatures in assembly, then output calls
        for call in fun.calls:
            time.sleep(0.02)
            if call not in prg.statlibs_dict.values():
                print('{} --|{}|--> {}'.format(fun.name, fun.calls[call], call))
                txt_f.write('{} --|{}|--> {}\n'.format(fun.name, fun.calls[call], call))
            else:
                print('{} --|{}|--> {} <=> {} --|{}|--> {}'.format(fun.name, fun.calls[call], call, fun.hash, fun.calls[call], [x.hash for x in prg.Functions if x.name == call][0]))
                txt_f.write('{} --|{}|--> {} <=> {} --|{}|--> {}\n'.format(fun.name, fun.calls[call], call, fun.hash, fun.calls[call], [x.hash for x in prg.Functions if x.name == call][0]))
            if call not in totals.keys():
                totals[call] = fun.calls[call]
            else:
                totals[call] += fun.calls[call]
        if fun.calls:
            print('')
            txt_f.write('\n')
    print('\nTotals:')

    # Output number of calls each subroutine makes to eachother
    for key in totals:
        if key in prg.statlibs_dict.values():
            print('{} calls to {} <=> {}'.format(totals[key], key, [x.hash for x in prg.Functions if x.name == key][0]))
            txt_f.write('{} calls to {} <=> {}\n'.format(totals[key], key, [x.hash for x in prg.Functions if x.name == key][0]))
        else:
            print('{} calls to {}'.format(totals[key], key))
            txt_f.write('{} calls to {}\n'.format(totals[key], key))
    txt_f.close()

    # Create and write to file the Control Flow Graph using above analytical information
    name = prg.name
    functions = prg.Functions
    for fun in functions:
        fun_f = os.path.join('results', prg.name, fun.name + '.disasm')
        with open(fun_f, 'w') as f:
            f.write('\n'.join(fun.disasm))
    G=pgv.AGraph(strict = True, directed = True, ranksep='2')
    G.node_attr['shape']='box'
    for fun in functions:
        G.add_node(fun.name, URL='{}.disasm'.format(fun.name))
    for fun in functions:
        for lib in fun.calls.keys():
            if lib in prg.statlibs_dict.values():
                G.add_edge(fun.name, lib, color='blue', label=fun.calls[lib])
            else:
                G.add_edge(fun.name, lib, color='red', label=fun.calls[lib])
    G.layout(prog='dot')
    graph_f = 'graph_{}.svg'.format(name)
    G.draw(graph_f)
    os.rename(graph_f, os.path.join('results', prg.name, graph_f))
    print('Generated graph_{}.svg'.format(name))

if __name__ == "__main__":


    print("\n\nThis is a pilot framework that can automate the analysis of PLC binaries.   We know that binaries of\nPLC's are running off of two principal components:   CoDeSys  and the native OS (NucleusOS or Embedded Linux).\n   So far, we have been able to determine that the native OS of the PLC has implementations of the network stack,\nand that CoDeSys is system agnostic.   However, CoDeSys does handle some client-side network operations in which\n is compiled into a single binary with thousands of functions.   We have not gotten so far as to know what is in-\nside these, but we can demonstrate here that we are able to extract application-level subroutines from PLC binaries\n as well as some system calls that are important in determining the network behavior of the PLC.   This network behavior\nwill be used to create honeypots in virtual environments that have similar reactions to events in the network com-\npared to their real counterparts. \n\n")

    path = raw_input("ABS path of PRG:   ")
    print(path)

    binary_analysis(path, True)
