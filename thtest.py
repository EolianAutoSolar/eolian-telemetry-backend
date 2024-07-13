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
    return input("Ingrese un mensaje: ")

def Producer():
    while True:
        dict = read_data()
        print(f'Working on {dict}')
        q.put(dict)
        print(f'Finished {dict}')
        q.task_done()

threading.Thread(target=Producer, daemon=True).start()

q.join()
print("Done")

g = [1,2,3]

def up(up):
    while True:
        g.append(7)
        time.sleep(0.1)

def show(g):
    while True:
        print(len(g))
        time.sleep(0.1)

mensaje = "ASDASD"
## - Considerando el mensaje como el estado global
## 1. Definir read data, que no tenga busy waiting -> [Producer] vicho
## 2. Scheduling y cola
##    - Definir 1 consumers -> dante
##    - Logica de scheduler para consumers: Cola -> ambos
# viernes
## TEST
while True:
    read_data = producer.read_data()
    if(read_data is not None):
        consumers = [1,2,3]
        while(consumer):
            # consumer -> ready
            # consumer.procesa
            # consumer -> done
            # eliminar consumer

threading.Thread(target=up, args=(g,)).start()
threading.Thread(target=show, args=(g,)).start()

