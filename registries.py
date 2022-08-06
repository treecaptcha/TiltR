
# [id, [arcu1, arcu2]]
reg = []

# all loops should poll this value
stop = False

max_angle = 45 / 180

angle_multiplier = 1 / max_angle


def register(idx: int, markers: list):
    reg.append([idx, markers])

def setAngle(degrees):
    global max_angle, angle_multiplier
    max_angle = degrees/180
    angle_multiplier = 1 / max_angle
