# std modules
import time

# third party module
import can

# local modules

locked = False
class Database(can.Listener):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        f = open(file=self.file_name, mode='w')
        f.write("timestamp,msg_id,data\n")
        f.close()

    def on_message_received(self, msg: can.Message) -> None:
        global locked
        while locked:
            time.sleep(0.2)
        locked = True
        f = open(file=self.file_name, mode='a')
        f.write("{},{},{}\n".format(msg.timestamp, msg.arbitration_id, msg.data.hex()))
        f.close()
        locked = False