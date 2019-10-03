# Tarea1-Distribuidos

 ### Integrantes:
 -Christopher Gilbert 201573597-2\
 -Jean González 201573517-4
 
## Actividad 1:
Para el despliegue de la arquitectura primero es necesario ingresar a la carpeta Actividad 1\
 `` cd Actividad\ 1/ `` \
para luego poder ejecutar\
  ``docker-compose build``\
y finalmente ejecutar\
  ``docker-compose up``\
\
Una vez levantada la arquitectura, el cliente comienza la comunicacion con el servidor donde, luego de el hand-shake, el cliente envia 20 mensajes en intervalos de 0.2 segundo. Los mensajes que envia el cliente son predefinidos puesto que ``docker-compose up`` no permite utilizar una consola interactiva para el ingreso de mensajes  \
\
Las carpetas cliente y server almacenaran los archivos respuesta.txt y log.txt respectivamente. Esto se logra utilizando volumes de tal manera que las carpetas y archivos dentro del container se sincronicen con la carpeta del host.

## Actividad 2:

Para el despliegue de la arquitectura primero es necesario ingresar a la carpeta Actividad 1\
 `` cd Actividad\ 2/ `` \
para luego poder ejecutar\
  ``docker-compose build``\
y finalmente ejecutar\
  ``docker-compose up``\
\
Al igual que en la actividad 1 el cliente realiza el hand shake con el servidor y envia los 20 mensajes predefinidos en intervalos de 1 segundo, los cuales serán almacenados en el nodo seleccionado aleatoriamente entre los que hayan contestado al heartbeat (realizado mediante multicast)\

Para el desarrollo de esta actividad se definen 2 redes en donde una de ellas es de uso exclusivo para la comunicacion cliente-servidor y la otra para la comunicación servidor-nodos.\

Para el almacenamiento de los archivos solicitados, se crearon carpetas para cada nodo, para el servidor y para el clienta, con el mismo fin que en la Actividad 1
