import cv2
from cv2 import aruco
import functions

arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_50)
arucoParams = aruco.DetectorParameters_create()

# cap = cv2.VideoCapture(0) # agafem video de la webcam 
cap = cv2.VideoCapture('./media/prova/prova2.MOV')  # obrim video del test

contador = 0
center = []
vector = []

# while True:   # si agafem video de la webcam
while (cap.isOpened()):                                     # mentre video obert
    ret, frame = cap.read()                                 # agafem frame del video
    frame_resized = functions.rescale_frame(frame, 0.25)    # fem resize i mostrem per pantalla
    cv2.imshow("Frame", frame_resized)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):   # tecla q per sortir
        break
    elif key == ord("k"):   # tecla k per agafar frame / imatge
        if ret == True:
            contador = contador + 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            (corners, ids, _) = aruco.detectMarkers(gray, arucoDict, parameters=arucoParams)    # detecta marcadors a la imatge      
            if len(ids) == 2:       # si 2 marcadors detectats
                center = []                    
                ids = ids.flatten()

                for i, corner in zip(ids, corners):
                    corners = corner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))    #extraiem cantonada dreta abaix
                    topLeft = (int(topLeft[0]), int(topLeft[1]))                #extraiem cantonada d'adalt esquerra

                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)   #calcul centre marcador
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)

                    center.append(cX)
                    center.append(cY)

                vectorline = ((center[0]-center[2], center[1]-center[3]))   # calculem vector entre centres dos marcadors
                if vectorline[0] < 0:
                    vector.append((-vectorline[1], vectorline[0]))          # 
                else:
                    vector.append((vectorline[1], -vectorline[0]))
            else:
                print("Error, no detectat dos marcadors")
                break
        
        cv2.imshow("Imatge " + str(contador), frame_resized)    # mostrem les imatges capturades
        if contador == 2:                                       # si dos imatges sortir
            break

cap.release()

print("Vector inicial: ")
print(vector[0])    # Vector inicial

print("Vector final: ")
print(vector[1])    # Vector final

# calcular angle entre vector inicial i vector final
angle = functions.angle_between(vector[0], vector[1])

print("Angle: " + str(angle))
