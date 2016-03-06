#!/bin/bash
function geteth() {
eths=""
expectipaddr=$1
/sbin/ifconfig | while read line
do
exists=`echo $line|grep 'Link encap'`

if [ -n  "$exists"  ]
then
macaddr=`echo $line | awk  '{print $5}' | tr -d ' '`
if [ ! $macaddr = "00:00:00:00:00:00" ]
then
eths=`echo $line | awk  '{print $1}' | tr -d ' '`
fi
fi
addr=`echo $line|grep 'inet'`
if [ -n "$addr" ]
then
ipaddr=`echo $line |awk '{print $2}'|cut -d ":" -f 2`

if [ "$expectipaddr" = "$ipaddr" ]
then
echo $eths
#echo $expectipaddr
exit 0
fi

fi
done
return $eths
}

#eth=`geteth`
#echo "xxxxx="$eth
