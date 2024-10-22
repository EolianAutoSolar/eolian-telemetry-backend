import threading
# from remote import RemoteSender

lista_de_consumo = []

condition = threading.Condition()

num_consumers = 0

def consumer(task):
    global num_consumers
    print('Consumer started')
    with condition:
        while not lista_de_consumo:
            print('Waiting for production')
            condition.wait()
        print(num_consumers)
        if num_consumers > 0:
            num_consumers -= 1
            task(lista_de_consumo[0])
        else:
            task(lista_de_consumo.pop())

def producer(func): # Ver otra condicion para que el producer no le quite la seccion critica al consumer
    print('Producer started')
    with condition:
        cans = func()
        lista_de_consumo.append(cans)
        print(f'Produced {lista_de_consumo[0]}')
        condition.notify_all()

# ejecuta los producers y consumers de forma concurrente:
# NOTA: actualmente, crea todos los procesos 1 vez por paquete,
# se podria mejorar agregando como argumento la cantidad de paquetes a procesar y creando todos los procesos solo 1 vez.
# Para esto hay que tener en cuenta si es posible tener +-1 mensaje (por interferencia) y si es posible, como manejar ese caso
def main_task(recv, consumers: list):
    global num_consumers
    num_consumers = len(consumers)-1

    consumer_threads = [threading.Thread(target=consumer, args=(c.use_data, ), daemon=True) for c in consumers]

    # consumer_thread_3 = threading.Thread(target=consumer, args=(sender.use_data,), daemon=True)
    producer_thread = threading.Thread(target=producer, args=(recv,))

    for ct in consumer_threads:
        ct.start()

    producer_thread.start()
    
    for ct in consumer_threads:
        ct.join()
    
    producer_thread.join()
