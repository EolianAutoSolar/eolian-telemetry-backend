# Tests

## Ejecutar tests/benchmarks

`python3 testing.py <escenario.can>`

## Descripción 

Para que el funcionamiento del sistema se considere "exitoso" se consideran los siguientes 2 criterios:

1. Baja latencia
2. Eficiencia (en realidad, que no colapse)

Para medir el comportamiento del sistema en ambos criterios, se proveen 2 escenarios de ejecución, que representan un tráfico alto de datos en un tiempo corto (1 minuto) y un tráfico de datos moderado durante un tiempo prolongado (5 minutos), respectivamente.

Para generar las métricas sobre cada criterio, se ejecuta una versión modificada de la telemetría, que es igual a la versión que se usaría en el caso real, con la diferencia de que esta versión, añade algunas instrucciones al programa para poder generar las mediciones de latencia y consumo de recursos.

<<<<<<< Updated upstream
## Escenarios

* Alto tráfico en 1 minuto: `archivo.can`
* Tráfico moderando en 5 minutos: `esc2.can`

=======
El programa utiliza redes virtuales can y esta pensado para ejecutarse en la RPI4 B+.

## Escenarios

Un escenario se representa mediante un archivo que registra el tráfico de una comunicación CANBUS en un intervalo de tiempo (generado usado `candump <channel> -l`). Se incluyen estos 2 escenarios:

* Alto tráfico en 1 minuto: `archivo.can`
* Tráfico moderando en 5 minutos: `esc2.can`

Pero también se puede extender la reserva de escenarios a testear pasándole el escenario al programa como `python3 testing.py <nuevo escenario>`. No importa su extensión, a los escenarios incluidos se les agrego la extensión `.can` porque deja en claro el contenido del archivo.

>>>>>>> Stashed changes

