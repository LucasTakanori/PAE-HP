**KALMAN FILTER SPECIFICATIONS**

1. High level design

El filtre de Kalman l'utitzarem per filtrar el soroll blanc del senyal que ens envia el gyroscopi. Aixó es molt important si volem aconseguir que el nostre projecte tingui un marge de error inferior a 0.1 graus, doncs el soroll provinent del giroscopi pot distorsiona la mesura exacta del sensor i conseqüentment la mesura es incorrecta i pot donar a lloc a errors més grans que 0.1 graus.

El filtre de kalman implementa un model predictiu del senyal i el convina amb el senyal que s'ha mesurat per fer una correció. Tant la mesura com la prediccio contenen soroll (assumim que es gaussià) que es caracteritzat per matrius de covariança. La correcció es calcula de tal manera que li dona més pes al senyal el qual la seva covariança es més petita, que en altre paraules vol dir que conté menys soroll.


<img width="290" alt="image" src="https://user-images.githubusercontent.com/101046951/204100886-96920426-f7ed-485c-af04-e25811b3d181.png">



El model queimplementarem al nostre filtre es basa en el moviment circular i uniforme perque el senyal que ens arriba del gyroscopi es la velocitat angular del robot, i el que ens interesa a nosaltres es extreure la posició angular del robot.



2. Low level design


<img width="309" alt="image" src="https://user-images.githubusercontent.com/101046951/205762086-a3c857af-292e-47e5-906f-c8165af54f81.png">

**-Input:**

El input del nostre filtre son les mesures 'brutes' que provenen del gyroscopi, pero el gyroscopi només ens dona mesures de la velocitat agular, i el nostre vector d'estat conté també la posició angular, llavors, abans de filtrar el senyal, s'ha d'integrar les mesures per extreure la informació amb una senzilla equació de moviment: X(k) = X(k-1) + V(k) * t  , sent t l'invers de la frequencia de mostreig. 
El nostre vector input quedaria de la següent forma: x(k,m) = [ X(k), V(k) ]

La mesura, com he dit anteriorment es bruta, es a dir que conte un error gaussia aditiu, que es el que intentem filtrar amb el filtre de kalman. Aquest error es modela amb la matriu de covariança de mesura **R**. Aquesta matriu de covariança es una matriu 4x4 que conte les covariaces de la posicio i la velocitat angular. Aquests valors son constants, i per aconseguir un bon funcionament del filtre es tenen que estimar. Nosaltres estimarem la matriu fent diferentes proves amb l'ajuda del equip Validació.


**-Predicció:**

Per fer la predicció del vector estat, tenim dos alternatives. La primera consisteix en utilitzar un model de moviment circular uniforme, considerant que l'acceleració es nula, es a dir, utilitzant la mostra que s'ha filtrat a l'instant previ, es prediu la mostra següent fent servir les equacions de moviment circular uniforme, considerant que la velocitat es constant. Aquestes equacions es modelen en la matriu de transició de process **F**:

<img width="228" alt="image" src="https://user-images.githubusercontent.com/101046951/205757309-bc2660f6-4e84-4def-b344-d8e321f9cece.png">*Sistema d'equacions de la predicció*

L'altre alternativa consisteix en utilitzar la informació que ens proporciona els encoders per fer la predicció. La velocitat angular també es pot extreure dels encoders, evidentment es una mesura que també conté un error gaussia aditiu, pero es una mesura independent a la mesura dels encoder i pot servir d'utilitat a l'hora de fer la predicció. Llavors la predicció ja no es faria fent servir un model de moviment circular uniforme, si no que directament s'agafa la mesura que porvé del encoders.

En qualsevol dels casos, la predicció també conte un error, i aquest error s'ha de modelar una altra vegada amb una matriu de covariança, la matriu de covariança del process **P**. Aquesta matriu s'actualitza cada iteració, així doncs la seva inicialització no es tant important.


**-Correcció:**

**-Output:**

(descripción en detalle del sistema de ecuaciones, explicar cuales son las matrices de transición, que efectos tiene la covarianza en el resulatdo del filtro y como podemos estimarla)



3. Uniform circular motion

Al implementar el filtre de kalman fem servir 2 parametres per a cada sensor: la posició i la velocitat angular. Obtenim mostres a una alta frequencia (al voltant de 200Hz) i el robot rota a una velocitat moderada (maxim 2rads/segon). Aixi doncs podem calcular la màxima varicaio de l'angle entre cada mostra del giroscopi: 200Hz -> 0,005s; per tant, màxima diferència d'angle entre mostres = 2*0,005 = 0,01 rads/mostra.

Aquesta baixa variació de l'angle entre mostres, junt amb les caracteristiques del motor i tracció de les rodes fan que es pugui aproximar la velocitat angular per a una constant sense ser necessari definir una acceleració. Això simplifica els calculs necessaris i les prediccions proporcionades pel filtre de kalman.

Per implementar aquest filtre de kalman hem fet ús d'una llibreria de python anomendada KalmanFilter, on es defineixen posteriorment les matrius necessaries per a dur a terme la implementació circular d'aquest

4. Developing the code in python

Per implemntar tot el digrama de blocs amb les respectives equacions farem servir la llibreria de python **Filterpy**. Aquesta llibreria ens facilita molt el nostre treball perquè ja implementa totes les equacions, nomes es te que inicialitzar indicant el ordre del vector estat, en el nostre cas es un vectro de dimensió 2, les matrius de transició i les matrius de covariança. Després el process iteratiu es fa mitjançant la trucada de algunes funcions.

**IMPORTANT!** Per fer servir aquesta llibreria, primer es té que descarregar fent servir la següent comanda:
```
pip install filterpy
```

(explicar porque usamos python y la libreria que vamos a hacer servir, además mencionar que hemos creado la clase Kalman que se inicializa de tal forma)


5. Tests
