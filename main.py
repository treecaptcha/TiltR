#!/usr/bin/env python
import math
import platform
import threading
from math import atan2
from time import time_ns

import cv2

import cli
import registries

# between 0 and 1
max_angle = 90 / 180

angle_multiplier = 1 / max_angle

# id:[x, y]
markerCords = {}

if platform.system() == "Linux":
    import linux as controller
else:
    print("Unknown os, unable to load controller")
    raise Exception("Unknown os")


def getMarker(idE):
    try:
        return markerCords[idE]
    except:
        return [0, 0]


def main():
    t1 = threading.Thread(target=cli.main, args=[controller])
    t1.start()

    arucoDictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
    arucoParameters = cv2.aruco.DetectorParameters_create()

    breakType: str = None

    # Start the video stream
    cap = cv2.VideoCapture(0)
    start_time = 0
    frame_rate = 30;
    i = time_ns();
    while (True):
        real_frame_rate = (1.0 / ((time_ns() - start_time) / 1000000000))
        start_time = time_ns()

        frame_rate = (real_frame_rate + frame_rate*30)/31;

        ret, frame = cap.read()

        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDictionary, parameters=arucoParameters)

        if not len(corners) == 0:
            ids = ids.flatten()

            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners

                # round stuff
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                centerX = int((topLeft[0] + bottomRight[0]) / 2.0)
                centerY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(frame, (centerX, centerY), 4, (0, 0, 255), -1)

                markerCords.update({markerID: [centerX, centerY]})

                cv2.putText(frame, str(markerID), (centerX, centerY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        ind = 0;
        for idef, [icord, icar] in registries.reg:
            ind = ind + 1
            cor1 = getMarker(icord)
            cor2 = getMarker(icar)

            angle = atan2(cor1[1] - cor2[1], cor1[0] - cor2[0]) / math.pi

            if angle > max_angle:
                angle = max_angle
            elif angle < -max_angle:
                angle = -max_angle

            angle = angle * angle_multiplier
            cv2.putText(frame, "Angle: " + str(round(angle * 100)) + "%", (20, 20 + ind * 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 0), 2)

            controller.update(idef, angle)

        controller.forwardVirts()
        cv2.putText(frame, "FPS:   " + str(round(frame_rate)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.imshow('TiltR', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            breakType = "internal"
            break

        if registries.stop == True:
            breakType = "external"
            break
    cap.release()
    cv2.destroyAllWindows()
    if breakType == "internal":
        controller.shutdown()
        cli.shutdown()


if __name__ == '__main__':
    main()
