class Database():
    def __init__(self, file_name: str) -> None:
        self.id = "DB"
        self.file_name = file_name
        f = open(file=self.file_name, mode='w+')
        f.write("timestamp,msg_id,data\n")
        self.f = f

    def use_data(self, data) -> None:
        # f.write("{},{},{}\n".format(msg.timestamp, msg.arbitration_id, msg.data.hex()))
        self.f.write(str(data)+'\n')
        self.f.flush()