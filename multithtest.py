import threading


lista_de_consumo = []

condition = threading.Condition()

c = 0

def consumer(task):
    global c
    print('Consumer started')
    with condition:
        while not lista_de_consumo:
            print('Waiting for production')
            condition.wait()
        task(lista_de_consumo[0])
        if c > 0:
            c -= 1
            print(f'Consumed {lista_de_consumo[0]}')
        else:
            print(f'Consumed {lista_de_consumo.pop()}')

def producer(recv): # Ver otra condicion para que el producer no le quite la seccion critica al consumer
    global c
    print('Producer started')
    with condition:
        c = 2
        x = recv()
        lista_de_consumo.append(x)
        print(f'Produced {lista_de_consumo[0]}')
        condition.notifyAll()

def main_task():
    consumer_thread_1 = threading.Thread(target=consumer)
    consumer_thread_2 = threading.Thread(target=consumer)
    consumer_thread_3 = threading.Thread(target=consumer)
    producer_thread = threading.Thread(target=producer)

    consumer_thread_1.start()
    consumer_thread_2.start()
    consumer_thread_3.start()
    producer_thread.start()
    
    consumer_thread_1.join()
    consumer_thread_2.join()
    consumer_thread_3.join()
    producer_thread.join()

if __name__ == '__main__':
    for i in range(10):
        main_task()