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
            pass
        elif query == 0x33:
            pass
        elif query == 0x37:
            pass
        elif query == 0x42:
            pass
        elif query == 0x43:
            pass
        elif query == 0x44:
            pass
        
        if idkelly == 0x000:
            pass
        elif idkelly == 0x001:
            pass