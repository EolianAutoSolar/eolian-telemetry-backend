import csv

from tools.operations import linear_map, voltage_transform

messages = {}

def msg_to_data(msg):
    data = []
    for i in range(len(msg)//2):
        data.append(int(msg[i:i+2], 16))
    return data

with open('vcan0.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    i = 0
    for row in reader:
        i += 1
        if(i == 1):
            continue
        
        timestamp = row[0]
        
        msg_id = row[1]
        
        data = row[2]
        
        query = msg_id >> 3
        
        idkelly = msg_id & 0b111
        
        datas = msg_to_data(data)
        
        if query == 0x1b:
            messages["brake"] = linear_map(datas[0], 0, 255, 0, 5)
            messages["tps"] = linear_map(datas[1], 0, 255, 0, 5)
            messages["operation_voltage"] = voltage_transform(datas[2])
            messages["vs"] = linear_map(datas[3],120, 134, 4.75, 5.25)
            messages["bplus"] = voltage_transform(datas[4])
        elif query == 0x1a:
            messages["Ia"] = datas[0]
            messages["Ib"] = datas[1]
            messages["Ic"] = datas[2]
            messages["Va"] = voltage_transform(datas[3])
            messages["Vb"] = voltage_transform(datas[4])
            messages["Vc"] = voltage_transform(datas[5])
        elif query == 0x33:
            messages["pwm"] = datas[0]
            messages["enable_motor_rotation"] = datas[1]
            messages["motor_temperature"] = datas[2]
            messages["controller_temperature"] = datas[3]
            messages["high_side_heat_sink"] = datas[4]
            messages["low_side_heat_sink"] = datas[5]
        elif query == 0x37:
            messages["mechanical_speed"] = datas[0]<<8 | datas[1]
            messages["current_controller"]  = datas[2]
            messages["error_mechanical_speed"]  = datas[3] <<8 | datas[4]
        elif query == 0x42:
            messages["throttle_switch"] = datas[0]
        elif query == 0x43:
            messages["brake_switch"]  = datas[0]
        elif query == 0x44:
            messages["reverse_switch"]  = datas[0]
        
        if idkelly == 0x000:
            pass
        elif idkelly == 0x001:
            pass