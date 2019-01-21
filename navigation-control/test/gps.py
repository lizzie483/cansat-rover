import time
from serial import Serial

port = "/dev/ttyAMA0"

serial = Serial(port)

GGA_TYPE = 'GGA'

def parse_nmea_sentence(sentence):
    parsed_sentence = {}
    values = sentence.split(',')
    parsed_sentence['type'] = values[0][3:]

    if parsed_sentence['type'] == GGA_TYPE:
        latitud = int(values[2][:2]) + float(values[2][2:]) / 60.0
        if values[3] == 'S':
            latitud = -latitud

        longitud = int(values[4][:3]) + float(values[4][3:]) / 60.0
        if values[5] == 'W':
            longitud = -longitud

        parsed_sentence['latitud'] = latitud
        parsed_sentence['longitud'] = longitud

    return parsed_sentence
    

while True:
    try:
        data = serial.readline()
        sentence = data.decode('utf-8')
        print(sentence)
        parsed_sentence = parse_nmea_sentence(sentence)
    
        if parsed_sentence['type'] == GGA_TYPE:
            print('%s,%s' %(parsed_sentence['latitud'], parsed_sentence['longitud']))
            print(parsed_sentence)
		
    except:
        print("loading")

    time.sleep(0.5)
