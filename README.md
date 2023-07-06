# Prototipo telemetría fenix

El código se estructura de la siguiente forma:
1. Iniciar canales de comunicación
2. Recibir mensajes de la red can
3. Redirigir el procesamiento de los mensajes, lo cual implica:
    * Mostrar datos en consola
    * Guardarlos en un archivo .csv.

El ambiente de pruebas se creó utilizando las redes vcan (virtual can). Se crearon 2 redes:
* vcan0: Red que contiene la comunicación del Kelly
* vcan1: Red que contiene la comunicación de los voltajes del Orion BMS.

Video de funcionamiento [en este link](https://youtu.be/AczRkLPMyjk).