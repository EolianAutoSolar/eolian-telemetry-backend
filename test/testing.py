import sys
import os
from multiprocessing import Process

def feed(scenario):
    # TODO: Agregar diferencia de delays con respecto al tiempo actual y el tiempo del archivo del escenario
    os.system("canplayer -I {} can_bridge=vcan0".format(scenario))

# ejecuta el pipeline del testing
def test(scenario):
    ## ejecutar feeder con el escenario en paralelo
    feeder = Process(target=feed, args=(scenario,))
    feeder.start()

    ## ejecutar el programa
    ## for f in use_data_funs:
    ##    def modded_f(data):
    ##        log_received_data_time
    ##        f(data)
    # main([funciones use data], [funciones recv])
    # main.run()
    # main
    feeder.join()

if __name__ == "__main__":

    scenario = 0
    try:
        scenario = sys.argv[1]
    except IndexError:
        print("ERROR: Ingrese un escenario --> python3 testing.py <escenario>")
        exit()

    print("Iniciando test para el escenario {}...".format(scenario))
    test(scenario)
    ## barra de progreso
    print("Test finalizado")
    