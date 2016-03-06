#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ftplib import FTP 
def ftp_down(): 
    ftp=FTP() 
    timeout=30
    port=21 
    ftp.connect('172.16.205.4',port,timeout) 
    ftp.login('','') 
    print ftp.getwelcome()#显示ftp服务器欢迎信息 
    ftp.cwd('pub/') #选择操作目录 
    bufsize = 1024 
    list=ftp.nlst()#获得目录列表
    for name in list:
        print(name)  #打印文件名称
    #filename = "100.txt"
    path='/Volumes/Data File/work_file/Python/Script' + name #文件保存路径
    f = open(path,'wb').write         # 打开要保存文件
    filename = 'RETR' + name   # 保存FTP文件
    #aftp.retrlines('RETR ' + name)
    ftp.retrbinary( filename,f.write,bufsize) # 保存FTP上的文件
    ftp.quit()                  # 退出FTP服务器
    print "ftp down OK" 
if __name__ == '__main__':
      
      ftp_down()
