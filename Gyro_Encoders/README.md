# Encoders
Un encoder es un dispositivo que produce señales, con las cuales podemos saber varios aspectos de un motor, como la posición, la dirección de giro y la velocidad; en nuestro caso, nuestrros encoders tienen canales $A, B$ y $I$; además de tener sus complementarios, los cuales son útiles para reducir el ruido del señal en el caso que tengamos que procesar la señal a una larga distáncia, el cual no es nuestro caso. Además cabe destacar qque el canal $I$, nos indica cuando se ha hecho una revolución completa del eje del encoder. En nuestro caso una revolución completa de la rueda de nuestro robot corresponde a 50 ticks del canal $I$.

Los ticks de los encoders, nos permiten determinar cuánto ha girado cada rueda (tanto la izquierda como la derecha). Como sabemos el radio de cada rueda, podemos usar los datos de ticks y los datos del radio de la rueda para determinar la distancia recorrida por cada rueda. Usando la siguiente ecuación:

$$\text{Distance a wheel has traveled} = 2 \pi\cdot\text{radius of the wheel} \cdot\frac{\text{number of ticks}}{\text{number of ticks per revolution}}$$

Conocer la distancia recorrida por cada rueda nos ayuda a determinar dónde se encuentra el robot en su entorno con respecto a una ubicación inicial. Este proceso se conoce como odometría.

## Odometria

Toda la información de esta parte está basada en  [A Primer on Odometry and Motor Control](https://ocw.mit.edu/courses/6-186-mobile-autonomous-systems-laboratory-january-iap-2005/resources/odomtutorial/) del MIT.

Llamamos $d_{left}$ a la distancia girada por la rueda izquierda sobre $\Delta t$, y $d_{right}$ es la misma medida para la rueda derecha. Con estas dos disancias podemos saber en el caso de que $d_{left}=d_{right}$ que el robot está yendo en línea recta. Si $d_{left}\gt d_{right}$ ha girado hacia la derecha, y si $d_{left}\lt d_{right}$ ha girado hacia la izquierda. Podemos usar estas medidas para calcular la traslación y la rotación.

Para simplificar, se asume que la velocidad de las ruedas es constante, lo cual introduce un pequeño error, el cual es negligible siempre y cuando $\Delta t$ sea pequeño. Esta suposición significa que nuestro robot siempre se desplaza a lo largo de un arco circular. La longitud de este arco, $d_{center}$ viene dada por la media de $d_{left}$ y $d_{right}$

$$ d_{center} = \frac{d_{left}-d_{right}}{2} $$

Diremos que la rotación en radianes sobre $\Delta t$ es $\phi$. Siendo $r_{left}$, la distancia entre el centro del arco de desplazamiento de nuestro robot y su rueda izquierda y $r_{right}$ la misma distancia para la rueda derecha. Por lo tanto tenemos que $d_{left} = \phi{ r_{left} }$ y $d_{right} = \phi{ r_{right} }$. También, $r_{left} = r_{left} + d_{wheels}$ donde $d_{wheels}$ es la distancia entre las ruedas del robot. Obteneiendo la siguiente ecuación:

$$ \phi = \frac{d_{right}-d_{left}}{d_{wheels}} $$

En resumen, nuestras equaciones de odometria para $(x^{'}, y^{'}, \theta^{'})$ se reducen a:

$$ \begin{array}{rcl}
x^{'} & = & x + d_{center}cos(\theta) \\
y^{'} & = & y + d_{center}sin(\theta) \\
\theta^{'} & = &  \theta + \phi
\end{array} $$


