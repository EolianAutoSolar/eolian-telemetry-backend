import threading
import time
import queue

###
### PRODUCTOR (maxima prioridad)    CONSUMIDOR (--)
### -- Mientras productor espera un mensaje -> Los consumidores se esten ejecutando
### -- Mientras no hayan mensajes leidos ni procesados, ambos procesos esperan
### + Asumiendo que el tiempo entre mensajes alcanza para que todos los consumidores se ejecuten
###

q = queue.Queue()


def read_data():
    return input("Ingrese un mensaje: \n")

def producer(qs):
    while True:
        dict = read_data()
        for q in qs:
            q.put(dict)

## - Considerando el mensaje como el estado global
## 1. Definir read data, que no tenga busy waiting -> [Producer] vicho
## 2. Scheduling y cola
##    - Definir 1 consumers -> dante
##    - Logica de scheduler para consumers: Cola -> ambos
# viernes

def use_data(data):
    print("Used data {}".format(data))

# TODO: comparar opciones:
# cada consumnameor accede a la queue
# el main process maneja la queue y le pasa un objeto a los consumnameores
def consumer(q, name):
    while True:
        data = q.get()
        print("C{} got data {}".format(name, data))

if __name__ == "__main__":
    n = 3
    consumer_queues = [queue.Queue(1) for i in range(n)]

    for i in range(n):
        threading.Thread(target=consumer, args=(consumer_queues[i], i)).start()
    
    producer(consumer_queues)
