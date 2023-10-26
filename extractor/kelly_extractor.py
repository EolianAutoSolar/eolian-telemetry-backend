import csv

def readCan0(data, timestamp, msg_id, data):
    pass

with open('can0.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    i = 0
    for row in reader:
        i += 1
        if(i == 1):
            continue
        
        timestamp = row[0]
        
        msg_id = row[1]
        
        data = row[2]