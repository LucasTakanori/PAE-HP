**KALMAN FILTER SPECIFICATIONS**

1. High level design

El filtre de Kalman l'utitzarem per filtrar el soroll blanc del senyal que ens envia el gyroscopi. Aixó es molt important si volem aconseguir que el nostre projecte tingui un marge de error inferior a 0.1 graus, doncs el soroll provinent del giroscopi pot distorsiona la mesura exacta del sensor i conseqüentment la mesura es incorrecta i pot donar a lloc a errors més grans que 0.1 graus.

El filtre de kalman implementa un model predictiu del senyal y el convina amb el senyal que s'ha mesurat per fer una correció. Tant la mesura com la prediccio contenen soroll (assumim que es gaussià) que es caracteritzat per matrius de covariança. La correcció es calcula de tal manera que li dona més pes al senyal el qual la seva covariança es més petita, que en altre paraules vol dir que conté menys soroll.


<img width="290" alt="image" src="https://user-images.githubusercontent.com/101046951/204100886-96920426-f7ed-485c-af04-e25811b3d181.png">



El model queimplementarem al nostre filtre es basa en el moviment circular i uniforme perque el senyal que ens arriba del gyroscopi es la velocitat angular del robot, i el que ens interesa a nosaltres es extreure la posició angular del robot.


2. Low level design


<img width="461" alt="image" src="https://user-images.githubusercontent.com/101046951/204526480-5fb30aed-b356-4ed2-9db4-fa94a2a831ca.png">


(descripción en detalle del sistema de ecuaciones, explicar cuales son las matrices de transición, que efectos tiene la covarianza en el resulatdo del filtro y como podemos estimarla)


3. Uniform circular motion

Al implementar el filtre de kalman fem servir 2 parametres per a cada sensor: la posició i la velocitat angular. Obtenim mostres a una alta frequencia (al voltant de 300Hz) i el robot rota a una velocitat moderada (maxim 2rads/segon). Aixi doncs podem calcular la màxima varicaio de l'angle entre cada mostra del giroscopi: 200Hz -> 0,005s; per tant, màxima diferència d'angle entre mostres = 2*0,005 = 0,01 rads/mostra.

Aquesta baixa variació de l'angle entre mostres, junt amb les caracteristiques del motor i tracció de les rodes fan que es pugui aproximar la velocitat angular per a una constant sense ser necessari definir una acceleració. Això simplifica els calculs necessaris i les prediccions proporcionades pel filtre de kalman.

Per implementar aquest filtre de kalman hem fet ús d'una llibreria de python anomendada KalmanFilter, on es defineixen posteriorment les matrius necessaries per a dur a terme la implementació circular d'aquest

4. Developing the code in python

(explicar porque usamos python y la libreria que vamos a hacer servir, además mencionar que hemos creado la clase Kalman que se inicializa de tal forma)


5. Tests
