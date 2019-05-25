#!/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: yangjunfei2146@gmail.com
#  File Name:
#  Description:
#  Edit History:
# ==================================================

import os,time,json
import pysnooper
import subprocess
# import scandir
from  os.path import isdir,join
from os import stat
#@pysnooper.snoop('/var/log/scanlog')
#@pysnooper.snoop()
def shell_cmd(cmd):
    subprocess.PIPE
    #cmd= 'ping -c %s -i %s %s' % (3,0.01, "172.16.205."+str(i)+"\n")
    P=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                 stdout = subprocess.PIPE,
                 stderr = subprocess.PIPE,
                 shell = True)
    P.stdin.close()
    P.wait()
    return  P.stdout.readlines()

def conv(f):
    lsfile = iter(os.listdir(f)) # 获取f目录下一级目录和文件
    datafile = [i for i in lsfile if isdir(join(f,i))] # 一级子目录
    filefile = list(set(lsfile)-set(datafile)) # datafile 目录下的文件
    return (f ,datafile ,filefile)

def walk(f):
    yield conv(f)
    for e in conv(f)[1]:
        tf = join(conv(f)[0],e) # 给目录名加上前导路径
        yield conv(tf)
        for a,b,c in walk(tf): # 遍历子目录的文件和目录
            for k in b:
                yield conv(join(a,k))


def File_Label_Portiait(json_file,f):
    '''
    file_info = {
        file_name: {
            'file_name': file_name,
            'file_createtime': f_ctime,
            'file_acctime': f_atime,
            'file_modifytime': f_mtime,
            'file_size': fsize 
        }
    }
    '''
    file_info = {}
    for i in walk(f):
        file_name = i[0]
        cmd = 'du -sh %s' % file_name
        statinfo = stat(file_name)
        f_ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(statinfo.st_ctime))
        f_atime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(statinfo.st_atime))
        f_mtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(statinfo.st_mtime))
        f_size =  shell_cmd(cmd)[0].split()[0]
        #print "file %s size is : %s" % (file_name, f_size)
        file_info[file_name] = { 'file_name': file_name, 
                                'file_createtime': f_ctime, 
                                'file_atime': f_atime, 
                                'file_modifytime': f_mtime, 
                                'file_size': f_size }
         
        
    #print "####file_info: %s" % file_info 
    with open(json_file,"a+") as j:
        j.writelines(json.dumps(file_info, indent = 4)) 


    


if __name__ == '__main__':
    f="/root/"
    json_file="file_info.json"
    '''
    conv(f)
    #for i in walk('/isilon/Data/'):
    for i in walk('/root/'):
        print i
    '''
    File_Label_Portiait(json_file,f)
