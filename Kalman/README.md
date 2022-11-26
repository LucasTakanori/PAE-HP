**KALMAN FILTER SPECIFICATIONS**

1. High level design

El filtre de Kalman l'utitzarem per filtrar el soroll blanc del senyal que ens envia el gyroscopi. Aixó es molt important si volem aconseguir que el nostre projecte tingui un marge de error inferior a 0.1 graus, doncs el soroll provinent del giroscopi pot distorsiona la mesura exacta del sensor i conseqüentment la mesura es incorrecta i pot donar a lloc a errors més grans que 0.1 graus.

El filtre de kalman implementa un model predictiu del senyal y el convina amb el senyal que s'ha mesurat per fer una correció. Tant la mesura com la prediccio contenen soroll (assumim que es gaussià) que es caracteritzat per matrius de covariança. La correcció es calcula de tal manera que li dona més pes al senyal el qual la seva covariança es més petita, que en altre paraules vol dir que conté menys soroll.

El model queimplementarem al nostre filtre es basa en el moviment circular i uniforme perque el senyal que ens arriba del gyroscopi es la velocitat angular del robot, i el que ens interesa a nosaltres es extreure la posició angular del robot.
(descripción general del funcionamiento del filtro, input, prediction, correction, circular motion)


2. Low level design

(descripción en detalle del sistema de ecuaciones, explicar cuales son las matrices de transición, que efectos tiene la covarianza en el resulatdo del filtro y como podemos estimarla)


3. Uniform circular motion

(justificación de usar un modelo uniform y circular con aceleración constante)

4. Developing the code in python

(explicar porque usamos python y la libreria que vamos a hacer servir, además mencionar que hemos creado la clase Kalman que se inicializa de tal forma)


5. Tests
