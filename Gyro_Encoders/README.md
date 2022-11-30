##Odometria
Toda la información de esta parte está basada en  [A Primer on Odometry and Motor Control] (https://ocw.mit.edu/courses/6-186-mobile-autonomous-systems-laboratory-january-iap-2005/resources/odomtutorial/) del MIT.
Para simplificar, se asume que la velocidad de las ruedas es constante, lo cual introduce un pequeño error, el cual es negligible siempre y cuando $\delta t$ sea pequeño. Esta suposición significa que nuestro robot siempre se desplaza a lo largo de un arco circular. La longitud de este arco, $d_center$ viene dada por la media de $d_left$ y $d_right$
