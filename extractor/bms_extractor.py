import csv
import sys
import os

def str_to_data(str):
    data = []
    
    for i in range(0, len(str), 2):
        data.append(int(str[i : i + 2], 16))
    return data

if not (os.path.exists("bms.csv")):
    with open('bms.csv', 'a', newline='') as bmsfile:
        writer = csv.writer(bmsfile)
        
        messages = ["timestamp","pack_soc","pack_current","pack_inst_voltage","pack_open_voltage","crc_checksum","pack_abs_current","max_voltage","min_voltage","crc_checksum","max_temp","id_max_temp","min_temp","id_min_temp","mean_temp","internal_temp","id_max_volt","id_min_volt","thermistor_module","lowest_thermistor","highest_thermistor","average_thermistor","numbers_of_thermistors_enabled","highest_thermistor_id","lowest_thermistor_id","thermistor_id_relative_to_all","thermistor_value","thermistor_id_relative_to_this"]
        
        writer.writerow(messages)

with open(sys.argv[1], 'r') as can1file:
    reader = csv.reader(can1file, delimiter = ',', quotechar = '"')
    
    i = 0
    
    for row in reader:
        i += 1
        
        if(i == 1):
            continue
        
        messages = []
        
        for _ in range(28):
            messages.append("N")
            
        timestamp = row[0]
        
        # el formato que entrega el can handler es
        # 0b aaaaaaaa bbb
        # donde las a representan la id del mensaje
        # y las b representan el identificador interno que maneja el
        # can handler para el bms
        msg_id = int(row[1])
        msg_id = msg_id >> 3
        
        data = row[2]
        
        datas = str_to_data(data)
        
        messages[0] = timestamp
        
        #TODO: Se deben añadir las operaciones correspondientes en la lineas comentadas, esas operaciones tambien faltan en el archivo orion.py
        #TODO: Quizas falta un mensaje para el msg_id 0x103
        
        if msg_id == 0x100:
            messages[1] = datas[0]
            messages[2] = datas[1] # Operacion con datas[2]
            messages[3] = datas[3] # Operacion con datas[4]
            messages[4] = datas[5] # Operacion con datas[6]
            messages[5] = datas[7]
        
        elif msg_id == 0x101:
            messages[6] = datas[0] # Operacion con datas[1]
            messages[7] = datas[2] # Operacion con datas[3]
            #messages[8] = datas[4] # Operacion con datas[5]
            messages[8] = datas[3]
            #messages[9] = datas[6]
            messages[9] = datas[5]
        
        elif msg_id == 0x102:
            messages[10] = datas[0]
            messages[11] = datas[1]
            messages[12] = datas[2]
            messages[13] = datas[3]
            messages[14] = datas[4]
            messages[15] = datas[5]
            messages[16] = datas[6]
            messages[17] = datas[7]
            
        elif msg_id == 0x103:
            messages[18] = datas[0]
            messages[19] = datas[1]
            messages[20] = datas[2]
            messages[21] = datas[3]
            messages[22] = datas[4]
            messages[23] = datas[5]
            messages[24] = datas[6]
        
        elif msg_id == 0x104:
            messages[25] = datas[0] # Operacion con datas[1]
            messages[26] = datas[2]
            messages[27] = datas[3]
            messages[19] = datas[4]
            messages[20] = datas[5]
            messages[23] = datas[6]
            messages[24] = datas[7]
        
        with open('bms.csv', 'a', newline='') as bmsfile:
            writer = csv.writer(bmsfile)
            
            writer.writerow(messages)