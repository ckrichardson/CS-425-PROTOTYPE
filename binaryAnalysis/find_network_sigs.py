import os


def find_syscalls(path):
    if not os.isfile(path):
        return "bad path"

    list_of_sys[] = []

    with open(path, "r") as inputfile:
        for line in inputfile:
            fields = line.split(" ")
            for element in fields:
                if "Sys" in element and element not in list_of_sys:
                    list_of_sys.append(element)

def find_network_syscalls(path):
    if not os.isfile(path):
        return "bad path"

    list_of_sys[] = []

    with open(path,"r" as inputfile:
            for line in inputfile:
            fields =  line.split(" ")
            for element in fields:
                if "Sys" in element and element not in list_of_sys:
                    list_of_sys.append(element)


