#!/bin/bash

if [ ! -d "$(grep //192.168.2.209/PiCamera /home/pi/sambashare)" ]; then
	sudo mount -t cifs -o ip=192.168.2.209,user=bob,password=hanyang1,rw,file_mode=0777,dir_mode=0777 //HAN-PC/PiCamera /home/pi/sambashare/
	sleep 30
fi

sudo mkdir -p /home/pi/sambashare/`date -d yesterday '+%d%m%y'`

cd /var/www/media   

for f in *.*
do 
   sudo mv -v  $f  /home/pi/sambashare/`date -d yesterday '+%d%m%y'`
done
