# !/usr/bin/env bash
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: yangjunfei2146@gmail.com
#  File Name: 
#  Description:
#  Edit History: 2019-06-06
# ==================================================

Config_file="ossutilconfig-genetronop"
Archive_file_index="result3"
EndPoint="oss://fsz-databackup/original_data/Taq/panel825/"
Archive_Log=logs/Archive-`date "+%Y-%m-%d"`-log
Archive_dir="/RawData_classed_EMC/Taq/panel825/*.yaml"
Archive_Files()
{
#  grep -w -e read1 -e read2  \
# /RawData_classed_EMC/Taq/panel825/P1904110013.yaml|\
# awk -F ':' '{print $2}' |awk -F '/' '{print $0," ",$NF}'
# 结果为：
# /RawData_classed_EMC/contingency_dir/panel825/W014575N_HJT2GDSXX-L1_R1.fastq.gz   W014575N_HJT2GDSXX-L1_R1.fastq.gz
 for i in `ls $Archive_dir`
 do
   grep -w -e read1 -e read2  $i |awk -F ':' '{print $2}' |awk -F '/' '{print $0," ",$NF}'
 done
}

# 我们需要通过 pip instll shyaml 安装 yaml 处理工具；
# 帮助文档，查看 https://linuxtoy.org/archives/shyaml.html 或者 
# https://github.com/0k/shyaml

# [ $(command -v shyaml > /dev/null 2>&1 && echo $?) -ne 0 ] &&  pip install shyaml
# 处理 yaml 
OSSCMD=$PWD/ossutil

list_dir()
{
 $OSSCMD -c $Config_file ls $EndPoint -d
}

upload_file()
{ 
  rm -f result.tmp
  line_num=`Archive_Files|tee result.tmp|wc -l|cut -d " " -f1`
  FG=1
  while [ $FG -le $line_num ];do
    if [ `pgrep ossutil|wc -l` -lt 15 ];then
      eval $(sed -n "${FG}p" result.tmp|awk '{printf("line1=%s;line2=%s;line3=%s;",$1,$2,$3)}')
      
      echo "------ `date "+%Y-%m-%d/%T"` ---- start --$line2 --" >> $Archive_Log && \
      #echo "dddddddddddddddddddd"
      $OSSCMD  -c $Config_file cp -ru $line1 $EndPoint$line2  --loglevel=info >> $Archive_Log  && \
      echo "--------`date "+%Y-%m-%d/%T"`------ end ---$line2-- " >> $Archive_Log &
      echo "This is $FG  file upload...." >> $Archive_Log
      let FG=$FG+1
    else
      sleep 2
    fi
  done 
}

upload_file
#list_dir
#Archive_Files
#Archive_Files|tee result.tmp| wc -l|cut -d " " -f1
