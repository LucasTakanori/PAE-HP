import cv2
from cv2 import aruco
import functions
import numpy as np

# Dictionary and parameters of the Aruco markers
arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_50)
arucoParams = aruco.DetectorParameters_create()

# Open the video
cap = cv2.VideoCapture('./media/provaGyro/IMG_9085.MOV')

contador = 0 
diccionari = {"Vector_inicial": [], "Vector_final": []}

while (cap.isOpened()):
    _ , frame = cap.read()                         # Take a frame from the video 
    frame_resized = functions.rescale_frame(frame, 0.25) # Resize the frame only to show it
    cv2.imshow("Frame", frame_resized)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):                             # if key 'q' is pressed -> exit
        break
    # if key 's' is pressed -> starts to process a part of the video
    elif key == ord("s"):
        contador += 1
        vector = []
        sumx = 0
        sumy = 0
        while True:
            functions.detectarMarcadors(cap,arucoDict,arucoParams,vector)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):     # if key 'q' is pressed -> exit
                break
            elif key == ord("s"):   # if key 's' is pressed -> stop processing video
                mean_vector = np.mean(vector, axis=0)
                
                if contador == 1:   # store the mean of the vector orientation (initial and final)
                    diccionari.update({"Vector_inicial": mean_vector})
                else:
                    diccionari.update({"Vector_final": mean_vector})
                break

        # Shows the image 
        cv2.imshow(f"Imatge {contador}", frame_resized)
        if contador == 2:
            break
cap.release()

# Calculate the angle between two vectors
angle = functions.angle_between(diccionari["Vector_inicial"], diccionari["Vector_final"])
print("Angle: " + str(angle))