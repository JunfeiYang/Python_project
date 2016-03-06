import sys

class StdoutLogger(object):
  def __init__(self, mode="w"):
    if isinstance(sys.stdout, StdoutLogger):
      self.old_stdout = sys.stdout.old_stdout
    else:
      self.old_stdout = sys.stdout
    self.logfile = "stdout_log.dat"
    self.mode = mode
    self.log = open(self.logfile, mode)

  def write(self, message):
    self.old_stdout.write(message)
    self.log.write(message)  


