import csv

def linear_map(value: int, min: int, max: int, tomin: int, tomax: int):
    m = (tomax - tomin) / (max - min)
    return m * (value - min) + tomin

def voltage_transform(value: int):
    return value / 1.84

def str_to_data(str):
    data = []
    for i in range(0, len(str), 2):
        data.append(int(str[i : i + 2], 16))
    return data

with open('vcan0.csv', 'r') as can0file:
    reader = csv.reader(can0file, delimiter = ',', quotechar = '"')
    i = 0
    
    for row in reader:
        i += 1
        
        if(i == 1):
            continue
            
        print(row)
        
        messages = []
        
        for _ in range(25):
            messages.append("N")
        
        timestamp = row[0]
        
        msg_id = row[1]
        
        data = row[2]
        
        query = int(msg_id) >> 3
        
        idkelly = int(msg_id) & 0b1
        
        datas = str_to_data(data)
        
        messages[0] = timestamp
        messages[1] = idkelly
        
        if query == 0x1b:
            messages[2] = linear_map(datas[0], 0, 255, 0, 5)
            messages[3] = linear_map(datas[1], 0, 255, 0, 5)
            messages[4] = voltage_transform(datas[2])
            messages[5] = linear_map(datas[3], 120, 134, 4.75, 5.25)
            messages[6] = voltage_transform(datas[4])
        elif query == 0x1a:
            messages[7] = datas[0]
            messages[8] = datas[1]
            messages[9] = datas[2]
            messages[10] = voltage_transform(datas[3])
            messages[11] = voltage_transform(datas[4])
            messages[12] = voltage_transform(datas[5])
        elif query == 0x33:
            messages[13] = datas[0]
            messages[14] = datas[1]
            messages[15] = datas[2]
            messages[16] = datas[3]
            messages[17] = datas[4]
            messages[18] = datas[5]
        elif query == 0x37:
            messages[19] = datas[0] << 8 | datas[1]
            messages[20]  = datas[2]
            messages[21]  = datas[3] << 8 | datas[4]
        elif query == 0x42:
            messages[22] = datas[0]
        elif query == 0x43:
            messages[23]  = datas[0]
        elif query == 0x44:
            messages[24]  = datas[0]
            
        with open('kelly.csv', 'a', newline = '') as kellyfile:
            print(messages)
            
            writer = csv.writer(kellyfile)
            
            writer.writerow(messages)