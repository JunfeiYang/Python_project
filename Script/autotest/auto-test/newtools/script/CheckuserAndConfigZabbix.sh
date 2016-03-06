#!/bin/bash
filepath=$1
#currentIP=`cat $filepath|tr -d ["\n"]`
#currentIP=$1
serverIP=$2
tarfile=$3
exist="false"

if [ ! $filepath ]
then
  echo "usage ./CheckuserAndConfigZabbix.sh IPFile serverIPAddr"
  exit 0
fi

if [ ! $serverIP ]
then
  echo "usage ./CheckuserAndConfigZabbix.sh IPFile serverIPAddr"
  exit 0
fi

if [ ! $tarfile ]
then
 tarfile="zabbix_agent.tar.gz"
fi

currentIP=`cat $filepath|tr -d ["\n"]`
echo "`cat /etc/passwd | awk -F: '$3>=500' | cut -f 1 -d :`" > temp
 exec 3< temp
while read line <&3
do
#echo "$line""++++"
if [ $line = "zabbix" ];
then 
echo "$line is already exists!"
exist="true"
fi
done
#echo "exists=$exist"
if [[ $exist = "false" ]];
then
/usr/sbin/useradd -m  zabbix
password="zabbix"
echo  "$password" | passwd --stdin "zabbix"
fi
yum -y install sysstat
#add task and reset it
./crontab.sh "* * * * * /home/zabbix/zabbix_agent/scripts/zabbix_vmstat_cron.sh"
./crontab.sh "* * * * * /home/zabbix/zabbix_agent/scripts/zabbix_iostat_cron.sh"
rm -rf temp
tar zxvf $tarfile -C /home/zabbix/
cd /home/zabbix/zabbix_agent
curdate=`date '+%Y.%m.%d-%H.%M%.S'`
mkdir -p /home/zabbix/zabbix_agent/log/
mkdir -p /home/zabbix/zabbix_agent/data
echo "" > /home/zabbix/zabbix_agent/log/zabbix_agentd.log
chown zabbix:zabbix /home/zabbix/zabbix_agent/log/zabbix_agentd.log
sed -i "s#LogFile=/tmp/zabbix_agentd.log#LogFile=/home/zabbix/zabbix_agent/log/zabbix_agentd.log#g" /home/zabbix/zabbix_agent/conf/zabbix_agentd.conf
if [ $serverIP ]; then
sed -i "s#Server=172.16.17.221#Server=$serverIP#g" /home/zabbix/zabbix_agent/conf/zabbix_agentd.conf
fi
if [ $currentIP ]; then
sed -i "s#Hostname=172.16.236.42#Hostname=$currentIP#g" /home/zabbix/zabbix_agent/conf/zabbix_agentd.conf
else
echo useage "./CheckuserAndConfigZabbix.sh $hostname $serverIP<optional>"
exit 1
fi
chown -R zabbix:zabbix /home/zabbix/*
#add the port and save rule
/sbin/iptables -A INPUT -p tcp --dport 10050 -j ACCEPT
/sbin/iptables -A OUTPUT -p tcp --dport 10050 -j ACCEPT
/sbin/iptables -A INPUT -p tcp --dport 10051 -j ACCEPT
/sbin/iptables -A OUTPUT -p tcp --dport 10051 -j ACCEPT
/etc/rc.d/init.d/iptables save

cd /home/zabbix/
#kill the zabbix service first
ps -ef |grep "zabbix_agentd"|awk '{print $2}'|xargs kill -9
echo "" > /home/zabbix/zabbix_agent/log/zabbix_agentd.log
./start.sh
#add service at system starts
chmod +x /home/zabbix/zabbixagent
mv /home/zabbix/zabbixagent /etc/rc.d/init.d/
chkconfig --del zabbixagent
chkconfig --add zabbixagent
chkconfig zabbixagent on
chkconfig --list zabbixagent
service zabbixagent start

ps -ef |grep "zabbix_agentd"
