import threading
import can
from database import Database
from can_reader import CanReader
from frontend import ConsoleVisualization
from remote import RemoteReceiver

lista_de_consumo = []

condition = threading.Condition()

c = 0

db = Database("mttest.txt")
front = ConsoleVisualization()
receiver = RemoteReceiver("/dev/ttyUSB0")

def consumer(task):
    global c
    print('Consumer started')
    with condition:
        while not lista_de_consumo:
            print('Waiting for production')
            condition.wait()
        if c > 0:
            c -= 1
            task(lista_de_consumo[0])
        else:
            task(lista_de_consumo.pop())

def producer(func): # Ver otra condicion para que el producer no le quite la seccion critica al consumer
    global c
    print('Producer started')
    with condition:
        c = 1
        cans = func()
        lista_de_consumo.append(cans)
        print(f'Produced {lista_de_consumo[0]}')
        condition.notifyAll()

def main_task():
    consumer_thread_1 = threading.Thread(target=consumer, args=(db.use_data,), daemon=True)
    consumer_thread_2 = threading.Thread(target=consumer, args=(front.use_data,), daemon=True)
    producer_thread = threading.Thread(target=producer, args=(receiver.read_data,))

    consumer_thread_1.start()
    consumer_thread_2.start()
    producer_thread.start()
    
    consumer_thread_1.join()
    consumer_thread_2.join()
    producer_thread.join()

if __name__ == '__main__':
    for i in range(10):
        main_task()