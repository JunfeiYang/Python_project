#!/bin/bash

today_date=`date "+%Y-%m-%d"`

swift_list="swift_list-${today_date}"

back_dir=`pwd`
backup_data_dir="data_backup"
container="andre-test"
log="$backup_data_dir/logs"
while true
do
    time=`date "+%H:%M"`
    if [ $time = "18:12" ];then
        cd $back_dir
        if [ -d $backup_data_dir ];then
            echo $backup_data_dir >> /dev/null
        else
            mkdir -p $backup_data_dir
        fi
        export OS_TENANT_NAME=services
        export OS_USERNAME=swift
        export OS_PASSWORD=swift
        export OS_AUTH_URL="http://10.10.0.200:5000/v2.0/"
        #swift list $container --lh 
        swift list $container --lh |grep $today_date > $swift_list
        grep "not found"  $swift_list
        flag = `echo $?`
        if [ $flag -ne 0 ];then
            echo "时间［$time］swift 列表生成功！！" >> $log
        else
            
            echo "时间［$time］swift 列表生成失败！！" >> $log
        fi
    

    else
        echo "工作时间未到，进入休息模式"
    fi
    sleep 6
    continue
done

echo $swift_list
