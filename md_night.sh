#!/bin/bash

NOW=$(date +%Y_%m_%d_%H_%M_%S)

sudo mkdir -p /home/pi/sambashare/MotionCapture/$NOW/

sudo cp $1 /home/pi/sambashare/MotionCapture/$NOW/

echo "md 0" > /var/www/FIFO
sleep 1
echo "ru 0" > /var/www/FIFO
sleep 1 

sudo raspistill -q 75 -ex night -hf -vf -awb incandescent -ev 10 -w 1296 -h 976 -t 4000 -tl 4000 -o /home/pi/sambashare/MotionCapture/$NOW/image%04d.jpg

echo "ru 1" > /var/www/FIFO 

sleep 7
echo "camera re-enabled"
echo "md 1" > /var/www/FIFO

python /home/pi/bin/motion/emaildirectory.py -d /home/pi/sambashare/MotionCapture/$NOW/ -s bobthesheep22@gmail.com -r bobthesheep22@gmail.com

echo "email sent"



#IF the second argument is empty, send email to other people
if [ -z "$2" ]
	then 
		python /home/pi/bin/motion/emaildirectory.py -d /home/pi/sambashare/MotionCapture/$NOW/ -s bobthesheep22@gmail.com -r dc_cn@yahoo.com
fi