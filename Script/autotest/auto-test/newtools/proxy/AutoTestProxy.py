#!/usr/bin/env python

import sys
sys.path.append("../")
from yoyosys.DataCellTest import *
from proxy_config import *
from twisted.internet import reactor, defer, threads
from twisted.web import server, resource
from twisted.python import context, log

import os
import json
import time
import uuid
sys.coinit_flags = 0
import socket
from urllib import *

REQUEST_ID = "REQUEST_ID"
VERSION="1.0"

class AutoTest(DataCellTest):
  def __init__(self):    
    DataCellTest.__init__(self)

  def do_getPCList(self, user_input):
    return str(pc_list)

class AutoTestProxy(resource.Resource):
  isLeaf = True
  
  def parse_qs(self, request):
    qs = unquote_plus(request.uri)[2:]
    d = {}
    items = [s2 for s1 in qs.split("&") for s2 in s1.split(";")]
    for item in items:
      try:
        k, v = item.split("=", 1)
      except ValueError:
        raise

      if v or keep_blank_values:
        k = unquote_plus(k.replace("+", " "))
        v = unquote_plus(v.replace("+", " "))
        if k in d:
          d[k].append(v)
        else:
          d[k] = [v]

    request.uri = qs
    request.args = d
    return d



  def set_request_id(self, request, request_id):
    request.args[REQUEST_ID] = request_id

  def get_request_id(self, request):
    return request.args[REQUEST_ID]

  def delegate_WMI(self, request):
    autotest = AutoTest()
    command = request.args['command'][0]   
    method = command.split()
    call = getattr(autotest, "do_" + method[0])

    ret = call(" ".join(method[1:]))
    if ret is None:
      ret = "command has been done successfully"
    
    return ret
      
  def return_success(self, result, request):
    response = dict()
    response["result"] = result
    response["request_id"] = self.get_request_id(request)
    response= json.dumps(response)
    log.msg("======= response for request[%s] \n%s\n ======================="%(self.get_request_id(request), response))
    request.setHeader("Content-Type", "text/plain; charset=utf-8")
    request.write(response)
    request.finish()

  def return_failure(self, err, request):
    log.err("======= response for request[%s] \n%s\n ======================="%(self.get_request_id(request), err))
    request.setResponseCode(500)
    request.write(r"%s"%str(err))  
    request.finish()     
        
  def render_GET(self, request):    
    reply = ''
    self.parse_qs(request)
    request_id = str(uuid.uuid1())
    log.msg("======= " + request.uri + " [request_id=%s] ======="%request_id)
    self.set_request_id(request, request_id)
  
    try:    
      command = request.args['command'][0]    
      log.msg("render_GET command=[%s]"%command)
      method_name = command.split()[0]
    except KeyError:
      request.setResponseCode(400)
      return "Miss 'command' parameters"

    if not hasattr(AutoTest, "do_" + method_name):
      request.setResponseCode(405)
      return "Unsupported command [%s]"%method_name

    deferred=threads.deferToThread(self.delegate_WMI, request)
    deferred.addCallback(self.return_success, request)
    deferred.addErrback(self.return_failure, request)      
    return server.NOT_DONE_YET
  
def start():
  welcome = r'''
===== Welcome to AutoTest Proxy =====
current process PID: [%d]
current verion: [%s]
Site starting on port: [%s]
Site parameter THREAD_POOL_SIZE: [%d]
=====================================
'''%(os.getpid(), VERSION, PROXY_SERVER, THREAD_POOL_SIZE)
  log.msg(welcome)
  reactor.suggestThreadPoolSize(THREAD_POOL_SIZE)
  PORT=int(PROXY_SERVER.split(":")[1])
  reactor.listenTCP(PORT, server.Site(AutoTestProxy()))
  reactor.run()

if __name__ == '__main__':
  argv = sys.argv
  argn = len(argv)
  if argn == 1:
    config_module = "config"
  elif argn == 2:
    config_module = argv[1].split(".")
    if len(config_module) > 2:
      print "Usage: python %s [config_module]"%argv[0]
      print "config_module must like that 'XXX.py' or 'XXX'"
      sys.exit(0)
    config_module = config_module[0]
  else:
    print "Usage: python %s [config_module]"%argv[0]
    sys.exit(0)

  for key, val in vars(__import__(config_module)).iteritems():
    if key.startswith('__') and key.endswith('__'):
      continue
    vars()[key] = val

  logmode = open(LOGFILENAME,'w')
  #logmode = sys.stdout
  log.startLogging(logmode)

  start()
