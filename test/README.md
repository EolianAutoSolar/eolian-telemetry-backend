# Tests

## Ejecutar tests/benchmarks

Primero se deben configurar las redes can, el script espera un archivo que contenga tráfico sobre la red virtual `can_bridge`.

Para configurarla, ejecutar:

1. `sudo ip link dev add can_bridge type vcan`
2. `sudo ip link set can_bridge up`

Es importante estar seguro de que el escenario que se le entregué al script de testing, tenga su tráfico asociado a la red específicada, si no, el programa de testing no recibirá ningún paquete y la métrica de cantidad de paquetes será errónea.

Ejecutar el script de testing con `python3 testing.py <escenario.can>`

Al ejecutar una prueba, se generarán 3 archivos de métricas:

1. `system_usage.log` -> Consumo de cpu y ram durante la prueba
2. `delays.csv` -> Delays para cada paquete (diferencia de timestamp canbus y timestamp al llamar a use_data en algun consumer)
2. `processings.csv` -> Tiempos de procesamiento de cada paquete (diferencia entre tiempo antes y despues de llamar a use_data en algun consumer)

NOTA: Para 1. idealmente se debe registrar la carga producida solamente por la telemetría, omitiendo el feeder y las métricas. Más
detalles en la implementación de `metrics.py->log_usage`.

## Descripción 

Para que el funcionamiento del sistema se considere "exitoso" se consideran los siguientes 2 criterios:

1. Baja latencia
2. Eficiencia (que la RPI no colapse ni en CPU o temperatura)

Para medir el comportamiento del sistema en ambos criterios, se proveen 2 escenarios de ejecución, que representan un tráfico alto de datos en un tiempo corto (1 minuto) y un tráfico de datos moderado durante un tiempo prolongado (5 minutos), respectivamente.

Para generar las métricas sobre cada criterio, se ejecuta una versión modificada de la telemetría, que es igual a la versión que se usaría en el caso real, con la diferencia de que esta versión, añade algunas instrucciones al programa para poder generar las mediciones de latencia y consumo de recursos.

El programa utiliza redes virtuales can y esta pensado para ejecutarse en la RPI4 B+.

## Escenarios

Un escenario se representa mediante un archivo que registra el tráfico de una comunicación CANBUS en un intervalo de tiempo (generado usado `candump <channel> -l`). Se incluyen estos 3 escenarios:

* Alto tráfico de datos durante 1 minuto: `1000hz1min50x4.can`
* Tráfico moderado de datos durante 5 minutos: `40hz5min40x4.can`
* Pequeño escenario para probar ejecución: `test.can`

También se pueden ejecutar escenarios personalizados, pasándole el escenario al programa como `python3 testing.py <nuevo escenario>`. No importa su extensión, a los escenarios incluidos se les agregó la extensión `.can` porque deja en claro el contenido del archivo.

Los nombres de los escenarios dados, se refieren a la frecuencia de envío de mensajes aproximada (delay configurado en los kelly handler del can_handler). Luego el tiempo de broadcast y finalmente el consumo máximo de CPU aproximado durante la generación de datos. Por ejemplo el escenario `40hz5min40x4.can` significa:

* Una prueba con una tasa de muestreo de ~40 mensajes por segundo
* Duración de transmisión de 5 minutos
* Consumo aproximado tope de 40% en los 4 cores.

En realidad la cantidad de mensajes será mayor, aproximádamente el doble, ya que cada kelly emite la respuesta de su mensaje al mismo tiempo. Además de que no se consideran los mensajes enviados por el BMS.


