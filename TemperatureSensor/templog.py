import sys
import Adafruit_DHT
import time
import math
import json
import shutil

sensor = Adafruit_DHT.AM2302
pin = 14
x = 0
maxEntry = 96
pollTime = 1800
isFilled = False

#Delete all content
def deleteContent(file):
	file.seek(0)
	file.truncate()

def deleteFirstLine(filename):
    with open(filename , 'a+') as f:
        lines = f.readlines()
        if len(lines) >= maxEntry:
            del lines[0]
            f.close()
            with open(filename , 'w') as f:
                f.writelines(lines)
                f.close()
        else:
            f.close()

while True:
    if x < maxEntry:
        humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
        if humidity is not None and temperature is not None:

            temperature = round(temperature , 2)
            humidity = round(humidity , 2)
            data = {"Temperature" : temperature, "Humidity" : humidity, "Time" : time.strftime("%Y/%m/%d_%H:%M:%S")}
            #log = [{"Temperature" : temperature, "Humidity" : humidity, "Time" : time.strftime("%Y/%m/%d_%H:%M:%S")}]

            #current temp log
            with open('/var/www/weatherdata/currenttemp.json', 'w') as h:
                json.dump(data,h, ensure_ascii=False)
            h.close()

	        #Temp/Hum log , cleared every 48 hours
            with open('/var/www/weatherdata/temphumlog.csv' , 'a+' ) as temphum:
                if x  == -1:
                    deleteContent(temphum)
                temphum.write('{0},{1},{2}\n'.format(temperature,humidity,time.strftime("%H:%M:%S_%d/%m/%Y")))
	        temphum.close()
            #Check if tempcycle log and hum cycle log is complete, if so delete first line of each log
            deleteFirstLine('/var/www/weatherdata/tempcycle.csv')
            deleteFirstLine('/var/www/weatherdata/humcycle.csv')

	        #Temperature cycled log
            with open('/var/www/weatherdata/tempcycle.csv' , 'a+' ) as tempcycle:
	            tempcycle.write('{0},{1}\n'.format(time.strftime('%Y,%m,%d,%H,%M,%S'),temperature))
       	    tempcycle.close()

	        #Humidity cycled log
            with open('/var/www/weatherdata/humcycle.csv' , 'a+') as humcycle:
                humcycle.write('{0},{1}\n'.format(time.strftime('%Y,%m,%d,%H,%M,%S'),humidity))

	        humcycle.close()

            x = x + 1
            time.sleep(pollTime)
    elif x >= maxEntry:
        isFilled = True
        destination = '/home/pi/sambashare/templog/'
        newdest = destination +  time.strftime("%Y%m%d_%H%M%S")
        shutil.copyfile('/var/www/js/templog.json', newdest )
        x = -1


