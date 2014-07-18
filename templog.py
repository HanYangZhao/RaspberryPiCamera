import sys
import Adafruit_DHT
import time
import math
import json
import shutil

sensor = Adafruit_DHT.AM2302
pin = 14
x = 0
maxEntry = 290
pollTime = 300

#Delete all content
def deleteContent(file):
	file.seek(0)
	file.truncate()


while True:
    if x < maxEntry:
        humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
        if humidity is not None and temperature is not None:

            temperature = round(temperature , 2)
            humidity = round(humidity , 2)
            data = {"Temperature" : temperature, "Humidity" : humidity, "Time" : time.strftime("%Y/%m/%d_%H:%M:%S")}
            log = [{"Temperature" : temperature, "Humidity" : humidity, "Time" : time.strftime("%Y/%m/%d_%H:%M:%S")}]

            with open('/var/www/js/tempdata.json', 'w') as h:
                json.dump(data,h, ensure_ascii=False)
            #f = open("TempMeasurements","a+" )
            #g = open("/var/www/TempMeasurements","w")
            with open('/var/www/js/templog.json' , 'a+' ) as f:
                num_lines = sum(1 for line in f)
                if num_lines >= maxEntry:
                    deleteContent(f)
                json.dump(log,f, ensure_ascii=False)
            #f.write('{0:.2f},{1:.2f},{2}\n'.format(temperature,humidity,time.strftime("%H:%M:%S_%d/%m/%Y")))
            #g.write('{0:.2f},{1:.2f},{2}\n'.format(temperature,humidity,time.strftime("%H:%M:%S_%d/%m/%Y")))
            x = x + 1
            h.close()
            #f.close()
            time.sleep(pollTime)
    elif x >= maxEntry:
        destination = '/home/pi/sambashare/templog/'
        newdest = destination +  time.strftime("%Y%m%d_%H%M%S")
        shutil.copyfile('/var/www/js/templog.json', newdest )
        x=0


