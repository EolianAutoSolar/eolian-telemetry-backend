import csv

def readCan0(data, timestamp, msg_id):
    pass

with open('vcan0.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    i = -1
    for row in reader:
        i += 1
        if(i == 0):
            continue
        
        msgs = []
        datas = []
        
        timestamp = row[0]
        
        msg_id = row[1]
        
        msgs.append(msg_id)
        
        data = row[2]
        
        datas.append(data)
        
        if(msg_id % 10 == 5):
            c = 1
            while(int(msgs[i - c] / 100) != int(msg_id / 100)):
                pass