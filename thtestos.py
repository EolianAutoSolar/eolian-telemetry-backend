import threading
import time
import queue
import can
from database import Database
from datetime import datetime

q = queue.Queue()
can_reader = can.Bus(interface='virtual', channel='vcan0', receive_own_messages=True)
messages = 0

def producer(qs):
    while True:
        try:
            data = can_reader.recv()
            for q in qs:
                q.put(data)
        except KeyboardInterrupt:
            exit()

db = Database("mttest.txt")

def consumer(q, name):
    global messages
    while True:
        data = q.get()
        db.use_data(data)
        messages += 1

if __name__ == "__main__":
    n = 1
    consumer_queues = [queue.Queue(1) for i in range(n)]

    # save threads to not be deleted by python gc
    consumer_threads = []
    for i in range(n):
        t = threading.Thread(target=consumer, args=(consumer_queues[i], i), daemon=True)
        consumer_threads.append(t)
        t.start()
    
    def feeder():
        while True:
            can_reader.send(can.Message(arbitration_id=0x111))
            time.sleep(1/40)

    t = threading.Thread(target=feeder, daemon=True)
    t.start()
    start = datetime.now()
    producer(consumer_queues)
    can_reader.shutdown()
    db.f.close()
    print("run {} seconds, processed {} messages".format((start-datetime.now()), messages))
