import can

class OrionParse(can.Listener):

    def __init__(self, frontend):
        self.__frontend = frontend

    def on_message_received(self, msg: can.Message) -> None:
        id = msg.arbitration_id
        data = msg.data
        parsed_message = {}
        if id == 0x100:
            parsed_message["pack_soc"] = data[0]
            parsed_message["pack_current"] = data[1:3]
            parsed_message["pack_inst_voltage"] = data[3:5]
            parsed_message["pack_open_voltage"] = data[5:7]
            parsed_message["crc_checksum"] = data[7]

            # Saving data for the frontend update
            self.__frontend.update(bms_soc=msg.data[0])
            self.__frontend.update(bms_vol=msg.data[3:5])
            self.__frontend.update(bms_amp=msg.data[1:3])
        elif id == 0x101:
            parsed_message["pack_abs_current"] = data[0:2]
            parsed_message["max_voltage"] = data[2:4]
            parsed_message["min_voltage"] = data[4:6]
            parsed_message["crc_checksum"] = data[6]
        elif id == 0x102:
            parsed_message["max_temp"] = data[0]
            parsed_message["id_max_temp"] = data[1]
            parsed_message["min_temp"] = data[2]
            parsed_message["id_min_temp"] = data[3]
            parsed_message["mean_temp"] = data[4]
            parsed_message["internal_temp"] = data[5]
            parsed_message["id_max_volt"] = data[6]
            parsed_message["id_min_volt"] = data[7]

            # Saving data for the frontend update
            self.__frontend.update(bms_tem=msg.data[4])
        print(parsed_message)