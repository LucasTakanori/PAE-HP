Els videos per fer la demo es troben a la carpeta de Drive ja que són massa grans per penjar aqui. Estan dins de [PAE]HP -> material intern -> Team 3 Validació -> Aruco, [aqui](https://drive.google.com/drive/folders/13qfh2iZuN18NB4eX2Uu5K_UMZ6QVMspi)

Descarregar carpeta 'media' del drive i descomprimir-la, descarregar els arxius que es vulguin probar (important tenir el arxiu functions.py). Per fer la demo, baixar-se el fitxer 'foto.py' o 'video.py' del github.

  ![carpetas](https://user-images.githubusercontent.com/113769445/204526254-da4efcfe-5b15-4d84-9277-850a7a2849be.PNG)   ![media](https://user-images.githubusercontent.com/113769445/204527013-2f5922fe-2665-4a50-aefb-e45a46b0c147.PNG)


En el mateix diretori ha d'estar el codi 'functions.py', 'foto.py' o 'video.py i la carpeta media descomprimida. Per fer la demo s'ha d'executar el script foto.py o el script video.py:
  - Si volem executar el script 'foto.py', un cop fem run cal prèmer la tecla 'k' per prendre la primera foto del video (posició inicial) i caldrà tornar a prèmer la tecla 'k' un altre cop quan s'hagi mogut el plat per prendre la última foto del video (posició inicial). Això calcularà l'angle i el mostrara per pantalla.
  - Si volem executar el script 'video.py', un cop fem run cal prèmer la tecla 'k' per començar a prendre un troç de video i tornar a prèmer la tecla 'k' per deixar d'agafar video de la posició inicial. Després tornar a prèmer tecla 'k' quan s'hagi mogut el plat per tornar a començar a prendre un troç de video i tornar a prèmer la tecla 'k' per deixar d'agafar video de la posició final.

**Important:** per executar el codi cal descarregar dues llibreries de python amb les següents comandes:
  - pip install opencv-python
  - pip install opencv-contrib-python
  
-----------------------------------------------------------------------------------------------------------------------------------------

Aquest directori conté els següents scripts:

## functions.py
El fitxer "functions.py" inclou únicament una serie de funcions que són de utilitat en els altres fitxers. Per exemple, la funció angle_between que calcula l'angle entre dos vectors o la funció rescale_frame que fa un resize de la imatge per mostar-la per pantalla.

## calc_angle.py
El fitxer "calc_angle.py" donat un video on es mostrin dos marcadors aruco, els detecta i calcula el seu centre. A partir d'aqui fa un vector entre els dos centres i calcula el vector normal que serà el vector orientació. Cal explicitar el vector de referencia amb el que volem calcular l'angle.

## foto.py / video.py
El dos fitxers "foto.py" i "video.py" funcionen de manera similar, el primer donat un video de la prova al premer la tecla 'k' agafa una primera foto d'on extreu el vector_inicial i al tornar a premer la tecla 'k' agafa una segona foto d'on extreu el vector_final i calcula l'angle entre els dos vectors. 
Pel que fa a "video.py" has de prèmer cada cop dos cops la tecla 'k' per agafar un troç de video on la plataforma esta quieta a la posició inicial i calcula la mitja del vector per tal d'obtenir el vector_inicial. Fa el mateix pel vector_final i després calcula l'angle entre els dos vectors.
