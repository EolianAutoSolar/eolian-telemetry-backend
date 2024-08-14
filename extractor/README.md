# Utilización de archivos extractor

El uso de ambos archivos (bms_extractor.py y kelly_extractor.py) es similar. Para su uso se requiere manejar los programas desde la terminal y desde ella ubicarse en el directorio extractor o donde se encuentren los programas respectivos, una vez ahí se debe ejecutar un comando que tenga la siguiente estructura:

python <nombre_del_programa_extractor> <nombre_del_archivo_csv_a_ser_procesado>

La estructura de los archivos csv que deben ser procesados por el programa extractor siguen un formato similar con tres columnas:

| timestamp | msg_id | data |
|-----------|--------|------|

La única diferencia entre los que se entregan para kelly y bms es que se entrega información distinta como por ejemplo el id del kelly en el caso de los kelly.

Los resultados de la ejecución se almacenarán en kelly.csv y bms.csv para kelly_extractor.py y bms_extractor.py respectivamente. Estos archivos se crearán terminada la ejecución.

## Ejemplo de uso:

python bms_extractor.py vcan1.csv