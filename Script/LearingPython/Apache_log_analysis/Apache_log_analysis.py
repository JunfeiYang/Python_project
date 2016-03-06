#!/usr/bin/env python
#_*_ coding: utf-8 _*_
import os
import time#读取配置文件的包
from ConfigParser import ConfigParser
import sys
configFile = os.path.join(sys.path[0],'config/config.cnf')
config = ConfigParser()#读取配置文件
config.read(configFile)
#config.get(section, opt)

errorRequestStatus=[404,403,500,502,505]
unsafeRequestUrl=["../../","/etc/passwd","jsp"]
fieldSeparator='<|>'

lastTime=time.strftime('%Y-%m-%d%H%M',time.localtime(time.time()))
#localPath="/root/apache_log/"
#localDataPath="/root/apache_log/data/"
#localPath="/home/ap/sfmon/Apache_log_analysis"
#localDataPath="/home/ap/sfmon/Apache_log_analysis/data/"
localPath="/Volumes/Data File/work_file/Python/Script/LearingPython/Apache_log_analysis"
localDataPath="/Volumes/Data File/work_file/Python/Script/LearingPython/Apache_log_analysis/data"

readLineNum=5000000
ipTopList=[]
urlTopList=[]
countNumberOfError=0
countWarring=0
nextMin = "2400"
#'20130809'
saveDate=time.strftime('%Y%m%d',time.localtime(time.time()))
def getSaveDate():
    #'20130809'
    return time.strftime('%Y%m%d',time.localtime(time.time()))
def getNowDate():
    #'2013-08-09'
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))
def getNowHour():
    #'0940'
    return time.strftime('%H%M',time.localtime(time.time()))
def getApachePath():
    import  socket
    #获取主机名
    hostname = socket.gethostname()

    return config.get(hostname[4:7].lower(),'weblogpath')
def getApachePathLog():
    #
    logpath=getApachePath()
    return logpath+'/access-'+ getNowDate() + '.log'
def getOutLog():
    #nowtime=getNowDate()
    return localDataPath+'/'+ getSaveDate() +'.cal'
def countListToDict(list):
    listset=set(list)
    dict={}
    dd=[]
    for i in listset:
        dict[i]=list.count(i)
        dd=sorted(dict.items(), key=lambda d:d[1],reverse=True)
    return dd[0:10]

accessLogFile=open(getApachePathLog(),'r')
flushFile=open(getOutLog(),'a')
while True:
    time.sleep(0.5)
    #apache日志文件
    list = accessLogFile.readlines(readLineNum)
    num=0    
    for l in list:
        num = num +1
        #进行切割 awk '{print $(0-10)}'
        line=l.split()
        logIp = line[0]
        logTimeHour = line[3][13:15]
        logTimeMin = line[3][16:18]
        logTimeSec = line[3][19:21]
        logRequestType = line[5].strip('"')
        logRequestUrl = line[6]
        try:
            logRequestStatus = int(line[8])
        except:
             logRequestStatus = 200
        logContentLength = line[9]
        overTime=time.strftime('%H%M%S',time.localtime(time.time()))
        try:
            logRefererUrl = line[10]
        except:
            logRefererUrl = '-'

        if nextMin == "2400":
            if logTimeHour+logTimeMin == "2359":
                logTimeMin = "00"
                logTimeHour = "00"
            if logTimeMin >= "01":
                nextMin = "0000"
        if logTimeHour+logTimeMin > nextMin or overTime == "235959":
            ipTopList.append(logIp)
            urlTopList.append(logRequestUrl)
            if logRequestStatus in errorRequestStatus:
                countNumberOfError +=1
            for unsafe in unsafeRequestUrl:
                if logRequestUrl.count(unsafe)>0:
                    countWarring+=1
            #print logRequestStatus,countNumberOfError,logRequestStatus in errorRequestStatus
            ipTopDict=countListToDict(ipTopList)
            urlTopDict=countListToDict(urlTopList)
            logcomm=nextMin[0:2]+":"+nextMin[2:4]+fieldSeparator+str(ipTopDict)+fieldSeparator+str(urlTopDict)+fieldSeparator+str(countNumberOfError)+fieldSeparator+str(countWarring)+"\n"
            #logcomm=nextMin[0:2]+":"+nextMin[2:4]+fieldSeparator+str(ipTopDict.keys())+fieldSeparator+str(ipTopDict.values())+fieldSeparator+str(urlTopDict.keys())+fieldSeparator+str(urlTopDict.values())+fieldSeparator+str(countNumberOfError)+fieldSeparator+str(countWarring)+"\n"
            flushFile.write(logcomm)
            ipTopList = []
            urlTopList = []
            countNumberOfError = 0
            countWarring = 0
            nextMin = logTimeHour+logTimeMin
        else:
            ipTopList.append(logIp)
            urlTopList.append(logRequestUrl)
            if logRequestStatus in errorRequestStatus:
                countNumberOfError +=1
            for unsafe in unsafeRequestUrl:
                if logRequestUrl.count(unsafe)>0:
                    countWarring+=1
            #print logRequestStatus,errorRequestStatus,countNumberOfError,int(logRequestStatus) in errorRequestStatus
    if getSaveDate() != saveDate:
        #print getApachePathLog()
        accessLogFile.close()

        ipTopDict=countListToDict(ipTopList)
        urlTopDict=countListToDict(urlTopList)
        logcomm=nextMin[0:2]+":"+nextMin[2:4]+fieldSeparator+str(ipTopDict)+fieldSeparator+str(urlTopDict)+fieldSeparator+str(countNumberOfError)+fieldSeparator+str(countWarring)+"\n"
        #logcomm=nextMin[0:2]+":"+nextMin[2:4]+fieldSeparator+str(ipTopDict.keys())+fieldSeparator+str(ipTopDict.values())+fieldSeparator+str(urlTopDict.keys())+fieldSeparator+str(urlTopDict.values())+fieldSeparator+str(countNumberOfError)+fieldSeparator+str(countWarring)+"\n"
        flushFile.write(logcomm)
        time.sleep(5)
        flushFile.close()

        ipTopList = []
        urlTopList = []
        countNumberOfError = 0
        countWarring = 0

        nextMin = "2400"

#        time.sleep(65)
        #print getApachePathLog()
        accessLogFile=open(getApachePathLog(),'r')
        flushFile=open(getOutLog(),'a')
        saveDate = getSaveDate()

