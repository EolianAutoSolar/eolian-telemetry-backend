# std modules
from typing import Any
import random
import time

# third party module
import can

# local modules
from tools.operations import linear_map, voltage_transform

def parsed_message_kelly(command: int, msg: can.Message):
    id = msg.arbitration_id
    data = msg.data
    parsed_message = {}
    if command == 0x1b:
        parsed_message["brake"] = linear_map(data[0], 0, 255, 0, 5)
        parsed_message["tps"] = linear_map(data[1], 0, 255, 0, 5)
        parsed_message["operation_voltage"] = voltage_transform(data[2])
        parsed_message["vs"] = linear_map(data[3],120, 134, 4.75, 5.25)
        parsed_message["bplus"] = voltage_transform(data[4])         # Resistance
    elif command == 0x1a:
        parsed_message["Ia"] = data[0]
        parsed_message["Ib"] = data[1]
        parsed_message["Ic"] = data[2]
        parsed_message["Va"] = voltage_transform(data[3])
        parsed_message["Vb"] = voltage_transform(data[4])
        parsed_message["Vc"] = voltage_transform(data[5])
    elif command == 0x33:
        parsed_message["pwm"] = data[0]
        parsed_message["enable_motor_rotation"] = data[1]
        parsed_message["motor_temperature"] = data[2]
        parsed_message["controller_temperature"] = data[3]
        parsed_message["high_side_heat_sink"] = data[4]
        parsed_message["low_side_heat_sink"] = data[5]
    elif command == 0x37:
        parsed_message["mechanical_speed"] = data[0]<<8 | data[1]
        parsed_message["current_controller"]  =data[2] #
        parsed_message["error_mechanical_speed"]  =data[3] <<8 | data[4] #
    elif command == 0x42:
        parsed_message["throttle_switch"] = data[0]
    elif command == 0x43:
        parsed_message["brake_switch"]  = data[0]
    elif command == 0x44:
        parsed_message["reverse_switch"]  = data[0]
    #print(parsed_message)
    return parsed_message

def request_kelly(bus, frontend):
    commands = [0x1b, 0x1a, 0x33, 0x37, 0x42, 0x43, 0x44]
    for c in commands:
        bus.send(
            can.Message(
            arbitration_id=0x64, data=[c], is_extended_id=False #respuesta 0x69
            )
        )
        bus.send(
            can.Message(
            arbitration_id=0xc8, data=[c], is_extended_id=False #respuesta 0xcd
            )
        )
        idrespond=[0x069, 0x0cd]
        while True:
            if len(idrespond)!=0:
                msg = bus.recv()
                if msg is not None:
                    response = parsed_message_kelly(c, msg) # 0x064 if msg.arbitration_id == 0x069 else 0x0c8 
                    if c == 0x33:
                            if msg.arbitration_id == 0x69:
                                frontend.update(kelly_izq_tem=msg.data[2])
                            else:
                                frontend.update(kelly_der_tem=msg.data[2])
                    elif c == 0x37:
                            if msg.arbitration_id == 0x69:
                                frontend.update(kelly_izq_kmh=msg.data[0]<<8 | msg.data[1])
                                frontend.update(kelly_izq_rpm=msg.data[0]<<8 | msg.data[1])
                            else:
                                frontend.update(kelly_der_kmh=msg.data[0]<<8 | msg.data[1])
                                frontend.update(kelly_der_rpm=msg.data[0]<<8 | msg.data[1])
                    idrespond.remove(msg.arbitration_id)
                    print(response)
                continue
            break
        time.sleep(0.01) #test