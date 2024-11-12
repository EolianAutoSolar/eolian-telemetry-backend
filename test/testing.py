import sys
import os
import psutil
import datetime
import time
from multiprocessing import Process, Event
import logging
from threading import Lock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database
from can_reader import CanReader
from frontend import ConsoleVisualization
from telemetry import main_task
from metrics import log_usage

# modificable
db = Database("mttest.txt")
front = ConsoleVisualization()
canreader = CanReader("vcan0")

delays = open("delays.csv", "w+")
delays.close()
delays_lock = Lock()

processings = open("processings.csv", "w+")
processings.close()
processings_lock = Lock()
# testing framework
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="log_file.log",  # Log file name
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TestConsumer():
    def __init__(self, consumer):
        self.consumer = consumer

    def use_data(self, data):
        
        # test info
        consumer_id = self.consumer.id
        can_frame = data["raw_message"]

        recv = datetime.datetime.now().timestamp()
        emit = can_frame.timestamp
        delay = recv - emit
        # TODO: Documentar unidades de medida del .log
        # Formato: RECV:Servicio|Delay=(Recv-Emitted)|Recv|Emmitted|Packet
        logger.info("RECV:{}|{}|{}|{}".format(
            consumer_id,
            delay,
            recv,
            emit,
            str(data)
        ))
        with delays_lock:
            with open("delays.csv", "a") as delays:
                delays.write("RECV:{}|{}|{}|{}\n".format(
                    consumer_id,
                    delay,
                    recv,
                    emit,
                    str(data)
                ))
        self.consumer.use_data(data)
        # Formato: USE:Servicio|Process_time=(Timestamp-Recv)|Timestamp|Packet
        end_timestamp = datetime.datetime.now().timestamp()
        process_time = end_timestamp - recv
        logger.info("PROCESS:{}|{}|{}|{}".format(
            consumer_id,
            process_time,
            end_timestamp,
            str(data)
        ))
        with processings_lock:
            with open("processings.csv", "a") as processings:
                processings.write("PROCESS:{}|{}|{}|{}\n".format(
                    consumer_id,
                    process_time,
                    end_timestamp,
                    str(data)
                ))

# cuenta la cantidad de frames canbus en el escenario entregado.
def count_packets(scenario) -> int:
    count = 0
    for line in open(scenario, 'r').readlines():
        # excluir ultima linea vacia '\n' o EOF
        if len(line) > 1:
            count += 1
    return count

def feed(scenario):
    # TODO: Agregar diferencia de delays con respecto al tiempo actual y el tiempo del archivo del escenario
    os.system("canplayer -I {} vcan0=vcan0".format(scenario))

# ejecuta el pipeline del testing
def test(producer, consumers, scenario):

    test_consumers = [TestConsumer(c) for c in consumers]

    ## registrar métricas del sistema
    stop_event = Event()
    metrics = Process(target=log_usage, args=(stop_event,))
    metrics.start()

    packets = count_packets(scenario)

    ## ejecutar feeder con el escenario en paralelo
    feeder = Process(target=feed, args=(scenario,))
    feeder.start()

    # ejecutar telemetría 
    for _ in range(packets):
        main_task(producer, test_consumers)

    # cerrar procesos
    stop_event.set()
    feeder.join()

if __name__ == "__main__":

    scenario = 0
    try:
        scenario = sys.argv[1]
    except IndexError:
        print("ERROR: Ingrese un escenario --> python3 testing.py <escenario>")
        exit()

    print("Iniciando test para el escenario {}...".format(scenario))

    test(
        producer=canreader.read_data,
        consumers=[db, front],
        scenario=scenario
    )

    delays.close()
    processings.close()

    ## barra de progreso
    print("Test finalizado")
    