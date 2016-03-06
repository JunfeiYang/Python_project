#!/bin/bash

l_dir=`pwd`
SERVERS_NAME=$1
DATE=$(date + "%Y-%m-%d")
DAY=$(DATE:8:2)
B2C_SERVERS_NAME=" ECS_B2C_WEB_0001 ECS_B2C_WEB_0002 ECS_B2C_WEB_0003 ECS_B2C_WEB_0004 ECS_B2C_WEB_0005 ECS_B2C_WEB_0006 ECS_B2C_WEB_0007 ECS_B2C_WEB_0008 ECS_B2C_WEB_0009 ECS_B2C_WEB_0010"
B2B_SERVERS_NAME=" ECS_B2B_WEB_0001 ECS_B2B_WEB_0002 ECS_B2B_WEB_0003 ECS_B2B_WEB_0004 ECS_B2B_WEB_0005 ECS_B2B_WEB_0006 ECS_B2B_WEB_0007 ECS_B2B_WEB_0008 ECS_B2B_WEB_0009 ECS_B2B_WEB_0010 ECS_B2B_WEB_0011 ECS_B2B_WEB_0012 ECS_B2B_WEB_0013"
SK_SERVERS_NAME=" ECS_SK_WEB_0001 ECS_SK_WEB_0002 ECS_SK_WEB_0003 ECS_SK_WEB_0004 ECS_SK_WEB_0005 ECS_SK_WEB_0006 ECS_SK_WEB_0007 ECS_SK_WEB_0008"
B2C_HTDOCS="/home/ap/ecp/apache2/htdocs/"
B2B_HTDOCS="/home/ap/ecp/ecp_web/web"
SK_HTDOCS="/home/ap/ecp/apache2/htdocs"
#REMOTE_COMMAND="exprot LANG=en_US;find /home/ap/ecp/apache2/htdocs/ -type f -print 0|xargs -0  -I{} md5sum '{}'|sort -k 2"
#REMOTE_COMMAND="exprot LANG=en_US;find /home/ap/ecp/apache2/htdocs/ -path /home/ap/ecp/apache2/htdocs/financemarket/img -prune  -o -type f -print |xargs md5sum '{}'|sort -k 2"

help(){
   echo "sh one.sh [b2c b2b sk all]"
}

if [ $# != 1 ];then
     help 
     exit 0
fi

if [[ "$1" == "all" ]];then
     line="md5";
else
     line=$1;
fi

case $1 in 
      all|ALL)
              SERVERS_NAME=$B2C_SERVERS_NAME$SK_SERVERS_NAME$B2B_SERVERS_NAME
              HTDOCS="$B2C_HTDOCS $B2B_HTDOCS $SK_HTDOCS"
              ;;
      b2b|B2B)
             SERVERS_NAME=$B2B_SERVERS_NAME
             
              ;;
      b2c|B2B)
             SERVERS_NAME=$B2C_SERVERS_NAME
             HTDOCS=$B2C_HTDOCS
              ;;
      sk|SK)
            SERVERS_NAME=$SK_SERVERS_NAME
            HTDOCS=$SK_HTDOCS
             ;;
      *)
            help
esac

REMOTE_COMMAND="export LANG=en_US;find $HTDOCS -type f print 0|xargs -0 -I{} md5sum '{}' |sort -k 2"

########
for server in $SERVERS_NAME
do
  #ssh $server "$REMOTE_COMMAND" &> $l_dir/$server.md5
  rsync_num=$(ssh $server ""ps aux|grep 'rsync --daemon'|grep -v grep |wc -l)
  http_num=$(ssh $server "netstat -lntp|grep http|wc -l")
  if [ "0"$rsync_num -eq 00 ] || [ "0"$http_num -eq 00];then
      echo -e "-->[SERVICE] $server \t rsync_num: $rsync_num \t http_num: $http_num"
  fi
done
##############

for i in `ls $l_dir |grep 1.md5|grep $line`;do
    a=`echo $i |awk -F '-' '{print $1}'`
    for b in `ls $l_dir|grep $a;`
    do
      num=`diff $i $b|wc -l`
      if [ $num -gt 118 ];then
          echo -e "-->[FILE] $b file error"
      else 
          echo -e "\t$b"
      fi

    done
done
















