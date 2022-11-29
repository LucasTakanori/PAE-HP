import cv2
from cv2 import aruco
import functions

# diccionari dels marcadors aruco
arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_50)
arucoParams = aruco.DetectorParameters_create()

# cap = cv2.VideoCapture(0)                         # si volem agafar la webcam del portatil
# Obrim el video de la prova
cap = cv2.VideoCapture('./media/prova/prova2.MOV')

contador = 0        
vector_inicial = []
vector_final = []

while True:
    ret, frame = cap.read()                         # Agafar frame del video
    # fem resize per mostrar el video per pantalla
    frame_resized = functions.rescale_frame(frame, 0.25)
    cv2.imshow("Frame", frame_resized)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):                             # tecla q per sortir
        break
    # tecla k per agafar part del video / tornar a clicar per acabar video
    elif key == ord("k"):
        contador = contador + 1
        vector = []
        sumx = 0
        sumy = 0
        while True:
            ret, frame = cap.read()
            frame_resized = functions.rescale_frame(frame, 0.25)
            cv2.imshow("Frame", frame_resized)
            # pasar frame en blanc i negre per millor deteccio
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            (corners, ids, _) = aruco.detectMarkers(
                gray, arucoDict, parameters=arucoParams)    # detecta marcadors al frame
            if ids is not None:                             # marcador detectat
                if len(ids) == 2:                           # si 2 marcadors detectats
                    center = []
                    ids = ids.flatten()

                    for i, corner in zip(ids, corners):     #
                        corners = corner.reshape((4, 2))
                        (topLeft, topRight, bottomRight, bottomLeft) = corners
                        bottomRight = (
                            int(bottomRight[0]), int(bottomRight[1]))
                        topLeft = (int(topLeft[0]), int(topLeft[1]))

                        # calcular centre marcador
                        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                        cY = int((topLeft[1] + bottomRight[1]) / 2.0)

                        center.append(cX)
                        center.append(cY)

                    # vector entre centres dels dos marcadors
                    vectorline = ((center[0]-center[2], center[1]-center[3]))
                    if vectorline[0] < 0:
                        # vector perpendicular
                        vector.append((-vectorline[1], vectorline[0]))
                    else:
                        vector.append((vectorline[1], -vectorline[0]))

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):  # tecla q per sortir
                break
            elif key == ord("k"):   # tecla k segon cop per tancar primer tall video
                # recorrer vector dels vectors directors dels marcadors i calcular la mitja
                for (x, y) in vector:
                    sumx = sumx + x
                    sumy = sumy + y
                if contador == 1:   # primer tall de video - vector inicial
                    vector_inicial = (sumx / len(vector), sumy / len(vector))
                else:
                    vector_final = (sumx / len(vector), sumy / len(vector))
                break

        # mostrar final imatge
        cv2.imshow("Imatge " + str(contador), frame_resized)
        if contador == 2:
            break

cap.release()

print("Vector inicial: ")   # Vector inicial
print(vector_inicial)

print("Vector final: ")     # Vector final
print(vector_final)

# calcular angle entre dos vectors
angle = functions.angle_between(vector_inicial, vector_final)

print("Angle: " + str(angle))
