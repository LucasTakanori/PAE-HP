import cv2
from cv2 import aruco
import numpy as np
import math


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)) * 180 / math.pi


def rescale_frame(frame, scale):    # works for image, video, live video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


def detectarMarcadors(cap, arucoDict, arucoParams, vector):
    _, frame = cap.read()  # it returns also ret but we don't need it
    # convert frame to black and white to improve the detection of the markers
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (corners, ids, _) = aruco.detectMarkers(
        gray, arucoDict, parameters=arucoParams)    # detect markers in the frame
    if ids is not None:                             # check if there is some marker detected
        if len(ids) == 2:                           # check if we have detected the 2 markers we need if not ignore the frame
            center = []
            ids = ids.flatten()
            for i, corner in zip(ids, corners):
                corners = corner.reshape((4, 2))
                # (topLeft, topRight, bottomRight, bottomLeft)
                (topLeft, _, bottomRight, _) = corners
                bottomRight = (
                    int(bottomRight[0]), int(bottomRight[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                # find the center (cX, cY) of the marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)

                # store the center in the array 'center'
                center.append(cX)
                center.append(cY)

            # calculate the vector between the 2 markers always in the same direction
            if (center[0] > center[2]):
                vectorline = ((center[0]-center[2], center[1]-center[3]))
            else:
                vectorline = ((center[2]-center[0], center[3]-center[1]))
            # add the vector in the list
            vector.append((-vectorline[1], vectorline[0]))
    # resize frame only to show the video
    frame_resized = rescale_frame(frame, 0.25)
    cv2.imshow("Frame", frame_resized)