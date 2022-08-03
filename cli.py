import os
import sys
import time

import registries

help: str = '''
help - show this page
list - refresh and show available controllers
bind - bind to a controller
stop - shutdown whole process
load - load configuration from save file
save - save configuration to save file
'''.strip()


# manages a cli
def main(controller):
    try:
        printControllers(controller)
        while(True):
            inpu = inp("cmd: ")
            inpus = inpu.split(" ")
            if inpu.startswith("list"):
                printControllers(controller)
            elif inpu.startswith("bind") and len(inpus) == 1:
                try:
                    dev = int(inp("device # (starts at 0): "))
                    ar1 = int(inp("marker 1: "))
                    ar2 = int(inp("marker 2: "))
                    a = controller.register(dev)
                    registries.register(a, [ar1, ar2])
                except:
                    print("Error!")

            elif inpu.startswith("stop"):
                registries.stop = True
                print("Shutting down...")
                return
            elif inpu.startswith("save"):
                out: str = controller.save()
                saveFile = open("save.dat","w")
                saveFile.write(out)
                saveFile.close()
            elif inpu.startswith("load"):
                saveFile = open("save.dat", "r")
                ine: str = saveFile.read()
                saveFile.close()
                controller.load(ine)
            elif inpu.startswith("help"):
                print(help)
            else:
                print(help)

    except:
        controller.shutdown()
        registries.stop = True
        raise

awaiting = False
def inp(pro: str):
    global awaiting
    awaiting = True
    a = input(pro)
    awaiting = False;
    return a

def printControllers(control):
    devs: [] = control.getDevices()
    for s in range(len(devs)):
        print(str(s) + ": " + str(devs[s]))


def shutdown():
    while(True):
        if awaiting:
            time.sleep(0.01) # if still in that state after 0.1 seconds
            if awaiting:
                os._exit(0)
        time.sleep(0.01)