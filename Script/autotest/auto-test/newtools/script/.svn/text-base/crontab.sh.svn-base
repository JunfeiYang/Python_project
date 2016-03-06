#!/bin/bash
add=$1

if [ ! "$add" ]
then
  echo " usage ./crontab.sh \"crontab-content"\"
  exit 0
fi

#exist="false"
function checkexist
{
cat /var/spool/cron/root|while read line
do
if [ "$line" = "$add" ]
then
echo "true"
#echo "duplicate line,the value you input is already exists!!!"
break
fi
done
}


exist=`checkexist`

if [  $exist ]
then
echo "duplicate line,the value you input is already exists!!!"
else
cat >> /var/spool/cron/root <<EOF
$add
EOF
fi
