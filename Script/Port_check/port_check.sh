#!/bin/bash
#

#########
#定义函数第一个参数
#Address(){
#   cat port.conf |while read line; do  echo $line; done|awk '{print $1}'
#}
#########
#定义函数的第二个参数
#Port(){
#   cat port.conf |while read line; do  echo $line; done|awk '{print $2}'
#}

#Address
#Port
cat port.conf |while read line1 line2; do  
#echo $line1 $line2; done
 python port_checker_tcp.py -a $line1 -p $line2

done

