# TODO: Update this following the refactor architechture and add it to main program
from telemetry_core import Process

class Database(Process):
    def __init__(self, file_name: str) -> None:
        self.data_buffer = ''
        self.counter = 0
        self.file_name = file_name
        f = open(file=self.file_name, mode='w')
        f.write("timestamp,msg_id,data\n")
        f.close()

    def use_data(self, data) -> None:
        self.data_buffer += data['raw_message'] + '\n'
        self.counter += 1
        if self.counter == 10:
            # print("saved data")
            f = open(file=self.file_name, mode='a')
            # f.write("{},{},{}\n".format(msg.timestamp, msg.arbitration_id, msg.data.hex()))
            f.write(self.data_buffer)
            f.close()
            self.data_buffer = ''
            self.counter = 0