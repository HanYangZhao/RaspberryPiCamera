TIP=192.168.2.253                           
                                               
ping -c4 ${TESTIP} > /dev/null               
                                               
if [ $? != 0 ]                               
then                                         
    logger -t $0 "WiFi seems down, restarting"
    ifdown --force wlan0                     
    ifup wlan0                               
else                                        
    logger -t $0 "WiFi seems up."           
fi                   
