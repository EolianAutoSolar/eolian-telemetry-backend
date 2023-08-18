# Pre Simu

Repositorio para simular comunicación CANBUS.

Considera:
* BMS lithiumate Pro
* Controladores Kelly
* (Pendiente) Orion BMS

## Modo de uso (solo linux)

1. Iniciar las redes con el comando `./can -u`
2. Ejecutar el simulador con el comando `./python3 pre_simu.py`

## Requerimientos

* Haber habilitado el módulo de [virtual can](https://www.pragmaticlinux.com/2021/10/how-to-create-a-virtual-can-interface-on-linux/).
* La libreria `python-can` de python (se instala con `pip3 install python-can`)

### Otros

Para borrar las redes virtuales ejecutar el comando `./can -d`.
