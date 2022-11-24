This directory contains the following scripts:

## functions.py
El fitxer "functions.py" inclou únicament una serie de funcions que són de utilitat en els altres fitxers.

## calc_angle.py
El fitxer "calc_angle.py" donat un video on es mostrin dos marcadors aruco, els detecta i calcula el seu centre. A partir d'aqui fa un vector entre els dos centres i calcula el vector normal que serà el vector orientació. Cal explicitar el vector de referencia amb el que volem calcular l'angle.

## take_fotos_video.py / take_video_video.py
El dos fitxers "take_fotos_video.py" i "take_video_video.py" funcionen de manera similar, el primer donat un video de la prova al premer la tecla 'k' agafa una primera foto d'on extreu el vector_inicial i al tornar a premer la tecla 'k' agafa una segona foto d'on extreu el vector_final i calcula l'angle entre els dos vectors. Pel que fa a "take_vide_video.py" has de prèmer cada cop dos cops la tecla 'k' per agafar un troç de video on la plataforma esta quieta a la posició inicial i calcula la mitja del vector per tal d'obtenir el vector_inicial. Fa el mateix pel vector_final i després calcula l'angle entre els dos.
