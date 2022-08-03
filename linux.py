import registries
from otherLicences.converter import toVirt
import evdev
from evdev import UInput, ecodes

# implements controller

# mapped remotes as [real, virt]
# forwardVirts() passes current state from real to virt
registry = []
# cached list of devices to prevent mismatch
currentDevices = [evdev.InputDevice(path) for path in evdev.list_devices()]


def register(id):
    real = currentDevices[id]
    virt = toVirt(real, len(currentDevices))

    print("Bound real " + str(real.path) + " to virtual " + str(virt.device.path) + "\nUse " + str(virt.device.path) + "in game")
    registry.append([real, virt])
    return len(currentDevices) - 1


# value is between -1 and 1
def update(idx, value):
    virt: UInput = registry[idx][1]
    virt.write(evdev.ecodes.EV_ABS, ecodes.ABS_TILT_X, round(value * 128 + 128))


def forwardVirts():
    for real, virt in registry:
        forward(real, virt)


# private
def forward(real: evdev.InputDevice, virt: UInput):
    a = real.read_one()
    while (a != None):
        virt.write_event(a)
        a = real.read_one()
    virt.syn()


# returns an abstract list of devices where only the index is relevant
def getDevices():
    currentDevices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    return currentDevices


saveFormat = "format: 1"


def save():
    dataFile = saveFormat + "\n"
    for ide, [arcu1, arcu2] in registries.reg:
        real: evdev.InputDevice = registry[ide][0]
        realPath = str(real.path)

        # should be using json, but I'm not getting paid for this
        data = realPath + ";" + str(arcu1) + ";" + str(arcu2) + "\n"
        dataFile = dataFile + data

    return dataFile


def load(text: str):
    lines: [str] = text.split("\n")
    if not lines[0].startswith(saveFormat):
        Exception("Version mismatch! got " + lines[0].replace("\n", "") + " expected " + saveFormat)
    lines.pop(0)
    for line in lines:
        a: [str] = line.split(";")
        try:
            real = evdev.InputDevice(a[0])
            virt = toVirt(real, len(currentDevices))
            registry.append([real, virt])
            ret = len(currentDevices) - 1
            registries.register(ret, [int(a[1]), int(a[2])])
            print("loaded")
        except:
            pass

def shutdown():
    for real, virt in registry:
        real.close()
        virt.close()