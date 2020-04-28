import os


def find_syscalls(path):
    if not os.path.isfile(path):
        return "bad path"

    list_of_sys = []

    with open(path, "r") as inputfile:
        for line in inputfile:
            fields = line.split(" ")
            for element in fields:
                if "Sys" in element and element not in list_of_sys:
                    list_of_sys.append(element)

    return list_of_sys

def find_network_syscalls(path):
    if not os.path.isfile(path):
        return "bad path"

    if ".analytics" not in path:
        return "bad file"

    list_of_sys = []

    with open(path,"r") as inputfile:
            for line in inputfile:
                fields =  line.split(" ")
            for element in fields:
                if "Sys" in element and element not in list_of_sys:
                    list_of_sys.append(element)
    return

if __name__ == "__main__":
    file_dir = os.path.dirname(os.path.realpath(__file__))
    print(find_syscalls(file_dir + "/100.analytics"))

