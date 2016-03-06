#!/usr/bin/env python
"""Friendly Python SSH2 interface."""
import os
import sys
import tempfile
import paramiko
import traceback

class Connection(object):
  """Connects and logs into the specified hostname.
  Arguments that are not given are guessed from the environment.""" 

  def __init__(self,host,username = None,password = None, port = 22, time = None):
    if not username:
      username = os.environ['LOGNAME']
    
    #templog = tempfile.mkstemp('.txt', 'ssh-')[1] #get the temp filename and log into temp file
    #paramiko.util.log_to_file(templog) #send the logs to logfile

    self._client = paramiko.SSHClient()
    self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection = self._client.connect(host, port, username, password, timeout = time)

    self._transport = self._client.get_transport()
    self._transport.set_keepalive(3)
    self._sftp = self._client.open_sftp()
    return connection

  def listdir(self, remotepath = '.'):
    """List all files."""
    return self._sftp.listdir(remotepath)

  def get(self, remotepath, localpath = None):
    """Copies a file between the remote host and the local host."""
    if not localpath:
      localpath = os.path.split(remotepath)[1]
    self._sftp.get(remotepath, localpath)

  def put(self, localpath, remotepath = None):
    """Copies a file between the local host and the remote host."""
    if not remotepath:
      remotepath = os.path.split(localpath)[1]
    self._sftp.put(localpath, remotepath)

  def execute(self, command, timeout = None):
    """Execute the given commands on a remote machine with stdout and stderr."""
    channel = self._transport.open_session()
    if timeout is not None:
      channel.settimeout(timeout)
    channel.get_pty()
    output = channel.makefile()
    channel.exec_command(command)
    return output.readlines()

  def close(self):
    """Closes the connection and cleans up."""
    self._client.close()
    self._client = None

  def __del__(self):
    """Attempt to clean up if not explicitly closed."""
    self.close()
    if self._client:
      self._client.close()
      self._client = None

def main():
  """Little test when called directly."""
  host = raw_input("host/ip:")
  username = raw_input("username:")
  password = raw_input("password:")
  myssh = Connection(host, username, password)
  print myssh.listdir()
  myssh.close()

if __name__ == "__main__":
  main()
