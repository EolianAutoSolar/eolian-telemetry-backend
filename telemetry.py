from multiprocessing import Process, Queue
from telemetry_core import Producer, Consumer


# Working implementation of a whole program execution using telemetry_core architechture
class Telemetry():

    def __init__(self, producer : Producer, consumer : Consumer) -> None:
        self.producer = producer
        self.consumer = consumer

    def run(self):
        queue = Queue(1)
        Process(target=self.producer.run, args=(queue,)).start()
        Process(target=self.consumer.run, args=(queue,)).start()