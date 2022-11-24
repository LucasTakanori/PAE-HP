import matplotlib.pyplot as plt
import numpy as np
import math

t = 5
fichero = 'bias.txt'
def lectura(fichero):
    f = open(fichero, 'r')
    datos = []
    for linea in f:
        #fem transformació per obtenir el resultat en graus
     datos.append(float(linea.strip('\n'))*(180/math.pi)*1.31*0.01)
    return datos

datos = lectura(fichero)
longitud = len(datos)
tiempo = np.arange(0, longitud*5, 5)
fig = plt.figure()
# plt.axis([0, 10, 0, 1])
plt.title('Bias', fontweight='bold')
plt.xlabel('Time')
plt.ylabel('Degrees/s')
plt.plot(tiempo, datos, 'k',label='noisy measurements')
plt.show()

print(datos)
print(longitud)
print(tiempo)
print(len(tiempo))
