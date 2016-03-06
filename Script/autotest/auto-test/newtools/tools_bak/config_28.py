#!/usr/bin/env python

#login config
pc_list =['172.16.236.28']
username = "root"
password = "password"

#yoyopkg config
release_home="/root/yoyopkg"
repository="https://172.16.205.130/repository"
repo_username="fu.haiwen"
repo_password="fu.haiwen"
platform="linux64d"

#bitsflow config
agent_list  = pc_list
agent_port = "21235"
agent2_port = "21235"
agent3_port = "21235"
agent_log_level="Info"

#groupd config
#groupd_list = ['172.16.205.181','172.16.205.156','172.16.205.183']
groupd_list = ['172.16.236.28']
groupd_service="5888"
groupd_log_level="Info"

#netvm config
netvm_list = ['172.16.236.28']
netvm_service    = "5678"
netvm_http_port  = "8456"
netvm_remote_dir = "remotes"
netvm_log_level="Info"

#datacell config 
datacell_list = pc_list
datacell_storage_home="/root/yoyopkg/storage"
datacell_volumes=["/mnt/sda1","/mnt/sdb1"]
datacell_log_home="/root/yoyopkg/logs"
datacell_conf_name="datacell.xml"
datacell_log_name="datacell.log"
datacell_pid_name="datacell.pid"
datacell_log_level="Debug"

#workflow && dsched config
workflow_list = ['172.16.236.28']
dsched_list = ['172.16.236.28']
workflow_groupname = "WORKFLOW"
dsched_groupname   = "DSCHED"
rpc_timeout = 10 #second
