# coding=utf-8
import cv2
from cv2 import aruco
import functions

arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_50)
arucoParams = aruco.DetectorParameters_create()

# cap = cv2.VideoCapture(0)                                           # llegir de la webcam
# cap = cv2.VideoCapture('./media/videos_iphone/video_markers.mov')   # llegir d'un video grabat
# cap = cv2.VideoCapture('./media/videos_xiaomi/video_markers.mp4')
cap = cv2.VideoCapture('./media/prova/prova5.MOV')

#while True:
while (cap.isOpened()):         # mentre video obert
    ret, frame = cap.read()
    if ret == True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        (corners, ids, _) = aruco.detectMarkers(gray, arucoDict, parameters = arucoParams)   # no utilitzem últim valor detectMarkers rejected
        ids = ids.flatten()
        center = [] # buidem el vector de punts centrics dels marcadors

        if len(ids == 2):

            for i, corner in zip(ids, corners):
                corners = corner.reshape((4,2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)

                center.append(cX)
                center.append(cY)
                
            if(len(center) > 3):                        # dibujar linea entre centro marcadores
                vectorline = ((center[0]-center[2],center[1]-center[3]))
                cv2.line(frame, (center[0],center[1]), (center[2],center[3]), (255,0,0), 4)
                puntomedio = (int((center[0]+center[2])/2),int((center[1]+center[3])/2))
                if vectorline[0] < 0:
                    orientacion = (-vectorline[1],vectorline[0])
                else:
                    orientacion = (vectorline[1],-vectorline[0])
            
            vector_referencia = (0, -1)
            angle = functions.angle_between(orientacion,vector_referencia)              # calcular angle entre dos vectors
            print("Angle: " + str(angle))
            cv2.putText(frame, "Angle: " + str(angle), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
            puntofinal = (int(puntomedio[0] + orientacion[0]), int(puntomedio[1] + orientacion[1]))
            cv2.line(frame, puntomedio, puntofinal, (0,255,0), 4)       
            print("Ids: " + str(ids)) 

        elif len(ids == 0):
            print("No es troba cap marcador")
        elif len(ids == 1):
            print("Només es troba el marcador: " + ids)
        else:
            print("Error")

    # MOSTREM LA IMATGE:

    # cv2.imshow("Frame", frame)

    frame_resized = functions.rescale_frame(frame, scale=.50)   # Sortida video finestra més petita amb una scale
    cv2.imshow("Frame_resized", frame_resized)                  # Mostrar sortida video finestra més petita
        
    key=cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()