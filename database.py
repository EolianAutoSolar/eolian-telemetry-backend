# TODO: Update this following the refactor architechture and add it to main program
from telemetry_core import Process

class Database(Process):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        f = open(file=self.file_name, mode='w+')
        f.write("timestamp,msg_id,data\n")
        self.f = f

    def use_data(self, data) -> None:
        # f.write("{},{},{}\n".format(msg.timestamp, msg.arbitration_id, msg.data.hex()))
        self.f.write("{},{},{}\n".format(data.timestamp, data.arbitration_id, data.data.hex()))
        self.f.flush()