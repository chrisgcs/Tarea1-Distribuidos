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
Una vez levantada la arquitectura, el cliente comienza la comunicacion con el servidor donde, luego de el hand-shake, el cliente envia 20 mensajes en intervalos de 1 segundo. Los mensajes que envia el cliente son predefinidos puesto que ``docker-compose up`` no permite utilizar una consola interactiva para el ingreso de mensajes  \
\
Las carpetas cliente y server almacenaran los archivos respuesta.txt y log.txt respectivamente\

## Actividad 2:
