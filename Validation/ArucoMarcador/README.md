# Aruco

El zip amb tot el projecte de Virtual Studio Code es troba penjat [aqui](https://drive.google.com/drive/folders/13qfh2iZuN18NB4eX2Uu5K_UMZ6QVMspi) al Drive perque encara sigui zip es massa gran i no deixa penjar-ho al Github.

## Instruccions

Executar el codi de "video.py" (comanda: python3 video.py). Sortira un video per pantalla, prèmer la tecla 'k' fer començar agafar primer video i tornar a premer 'k' per acabar d'agafar el primer troç de video. Repetir al final del video per agafar el segon troç. Automàticament mostrarà angle per pantalla al terminal.

Prèmer la tecla 'q' en qualsevol moment per sortir del video.


## Codi

Si nomes voleu fer un cop d'ull al codi, teniu el codi directament aqui penjat. Per executar-lo can instalar previament les llibreries opencv-python i opencv-contrib-python amb la comanda pip install opencv-python i pip install opencv-contrib-python. Cal descarregar-se algun video també que trobarem a la carpeta del drive de PAE HP dins la carpeta videos. Dins de video.py caldra canviar el path cap a aquest video que acabem de descarregar, si esta al mateix directori a cap = cv2.open("./nomVideo.MOV").
