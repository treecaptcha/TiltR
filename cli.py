import os
import subprocess
import sys
import time


import registries

help: str = '''
help - show this page
list - refresh and show available controllers
bind - bind to a controller
angm - set max angle
dump - dump info
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
            elif inpu.startswith("bind"):
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
            elif inpu.startswith("angm"):
                registries.setAngle(int(inp("max angle (0-180): ")))
            elif inpu.startswith("help"):
                print(help)
            elif inpu.startswith("dump"):
                print("----Start of from controller.dump()----")
                print(controller.dump())
                print("----End of from controller.dump()----")
                print("Python " + sys.version.replace("\n", "") + " for " + sys.platform)
                print("Paths: " + str(sys.path))
                try:
                    print("git: " + subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip())
                except:
                    # dunno what Windows does when it doesn't exist
                    print("git: unknown")
            else:
                print(help)

    except:
        print("unhandled exception, attempting to shut down ")
        controller.shutdown()
        registries.stop = True
        raise

awaiting = False
def inp(pro: str) -> str:
    global awaiting
    awaiting = True
    a = input(pro)
    awaiting = False;
    return a

def printControllers(control):
    devs: [] = control.getDevices()
    for s in range(len(devs)):
        print(str(s) + ": " + str(devs[s]))


def shutdown(wait = 0):
    time.sleep(wait)
    i = 0
    while(i < 500):
        if awaiting:
            i = i + 1;
            if awaiting:
                os._exit(0)
        time.sleep(0.01)
    print("over 5 seconds has been spent trying to shut down. Forcibly shutting down.")
    os._exit(1)