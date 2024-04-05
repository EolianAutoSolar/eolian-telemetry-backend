import csv

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
        
        if query == 0x1b:
            pass
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