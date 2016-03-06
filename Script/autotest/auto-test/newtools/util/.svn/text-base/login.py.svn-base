#!/usr/bin/env python
import ssh
import sys
import os
import threading
import time
import traceback

from threadpool import ThreadPool
from threadpool import makeRequests


login_pclist = []
login_connections = {}

class Login:
  def __init__(self, loginInfo, username, password, threadNum):
    self.threadNum = threadNum
    try:
      if isinstance(loginInfo, list):
        loginInfo = list(set(loginInfo))
        self.username = username
        self.password = password
        self.startWork(self.__createConnection, loginInfo)
      elif isinstance(loginInfo, dict):
        self.loginDict = loginInfo
        self.startWork(self.__createConnectionByLoginDict, loginInfo.keys())
      else:
        raise Exception, "loginInfo must be list or dict"
    except:
      print sys.exc_info()
    finally:
      pass

  def __createConnectionByLoginDict(self, pc):
    global login_connections
    global login_pclist
    try:
      loginInfo = self.loginDict[pc].split(':')
      username = loginInfo[0]
      password = loginInfo[1]
      connection = ssh.Connection(pc, username, password)
      login_connections[pc] = connection
      login_pclist.append(pc)
      print "create connection to %s successful." %pc
    except:
      print sys.exc_info()
      print "create connection to %s failed." %pc

  def __createConnection(self, pc):
    global login_connections
    global login_pclist
    try:
      connection = ssh.Connection(pc, self.username, self.password)
      login_connections[pc] = connection
      login_pclist.append(pc)
      print "create connection to %s successful." %pc
    except:
      print sys.exc_info()
      print "create connection to %s failed." %pc

  def startWork(self, work, argsList, resultCallback=None):
    try:
      requests = makeRequests(work, argsList, resultCallback, None)
      job = ThreadPool(self.threadNum)
      for req in requests:
        job.putRequest(req)
      job.wait()
    except:
      print sys.exc_info()
  
  def singleExecute(self,pc,cmd):
    global login_connections
    global login_pclist
    outputs = ""
    if login_connections.has_key(pc):
      outputs=(login_connections[pc]).execute(cmd)
    else:
      print "%s hasn't been initialized."%pc
    return outputs
     
  def serialExecute(self, cmd, input_pcList=None):
    global login_pclist
    self.cmd = cmd 

    if input_pcList is None:
      pcs = login_pclist
    else:
      pcs = input_pcList

    for pc in pcs:
      print "======== target: %s ========"%pc
      outputs = self.sameExecute(pc)
      for output in outputs:
        print output.rstrip("\n")
      print "======== end ========\n"

  def sameExecute(self, pc):
    return self.singleExecute(pc, self.cmd)

  def parallelExecute(self,cmd, input_pcList=None):
    global login_pclist
    self.cmd = cmd

    if input_pcList is None:
      pcs = login_pclist
    else:
      pcs = input_pcList

    self.startWork(self.sameExecute, pcs)

  def __putFile(self, pc):
    global login_connections
    try:
      login_connections[pc].put(self.localFile, self.remoteFile)
    except:
      print "putFile [%s] to [%s:%s] error." %(self.localFile, pc, self.remoteFile)

  def putFileToPC(self, localFile, remoteFile, pc):
    global login_connections
    try:
      login_connections[pc].put(localFile, remoteFile)
    except:
      print "putFile [%s] to [%s:%s] error." %(localFile, pc, remoteFile)

  def putFile(self, localFile, remoteFile=None):
    global login_pclist
    self.localFile  = localFile
    self.remoteFile = remoteFile
    self.startWork(self.__putFile, login_pclist)

  def __getFile(self, pc):
    global login_connections
    try:
      login_connections[pc].get(self.remoteFile, pc+"-"+self.localFile)
    except:
      traceback.print_exc()
      print "getFile [%s] from [%s] error." %(self.remoteFile, pc)

  def getFileFromPC(self, remoteFile, localFile, pc):
    global login_connections
    try:
      login_connections[pc].get(remoteFile, localFile)
    except:
      print "getFile [%s] from [%s] error." %(remoteFile, pc)

  def getFile(self, remoteFile, localFile=None, pclist=None):
    global login_pclist
    
    self.remoteFile = remoteFile

    if localFile==None:
      self.localFile = os.path.basename(remoteFile)
    else:
      self.localFile = localFile
    
    if pclist==None:
      pclist = login_pclist

    self.startWork(self.__getFile, pclist)
 
  def uploadAndExtractFile(self, pc):
    global login_connections
    print "\n====== IP: " + pc + " uploadAndExtractFile ======"
    if login_connections.has_key(pc):
      outputs=self.singleExecute(pc, "uname -a")
      for output in outputs:
        if output.find("x86_64") >= 0:
          srcFile = self.file64
        else:
          srcFile = self.file32

        try:
          login_connections[pc].put(srcFile, "%s/%s"%(self.installPath, srcFile))
          print "putFile[%s] to %s ok.\n" %(srcFile, pc)
        except:
          print "putFile[%s] to %s error.\n" %(srcFile, pc)
          continue

        try:
          self.singleExecute(pc, "cd %s;%s %s"%(self.installPath, self.extractCmd, srcFile))
          print "extract %s on %s ok\n"%(srcFile, pc)
        except:
          print "extract %s on %s error\n"%(srcFile, pc)
    else:
      print "%s hasn't been initialized."%pc

  def uploadAndExtractFiles(self, file32, file64, installPath, extractCmd):
    global login_pclist
    self.file32 = file32
    self.file64 = file64
    if installPath[-1] == "/":
      installPath = installPath[:-1]
    self.installPath = installPath
    self.extractCmd  = extractCmd
    self.startWork(self.uploadAndExtractFile, login_pclist)
