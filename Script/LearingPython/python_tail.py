#coding=utf-8
'''
    author:the5fire
    blog:http://www.the5fire.com
    date:2012-07-03
'''
import sys
already_print_num = 0

def get_last_line(filepath):
    '''
       获取未输入的行
    '''
    global already_print_num
    import  os
    if not os.path.exists(filepath):
       print 'no such file %s' % filepath
       sys.exit()
       return
    readfile = open(filepath, 'r')
    lines = readfile.readlines()

    if len(lines) > 20 and already_print_num == 0:
       #last_num = 20  #首次输出最多输出20行
       #经nonoob指正，修改如下
       already_print_num = len(lines) - 20
       
    if already_print_num < len(lines):
       print_lines = lines[already_print_num - len(lines):]
       for line in print_lines:
           print len(lines), already_print_num, line.replace('\n','')
       already_print_num = len(lines)
    readfile.close()

    
def timer(filename):
    '''
       每隔1秒执行一行                                                         '''
    while True:
          get_last_line(filename)
          import time
          time.sleep(1)
if __name__ == '__main__':
  if len(sys.argv) < 2:
     print 'illegal params'
     print '''
              ###########################################
              # Usage:  python_tail  filename           #
              # Example:python_tail  /var/log/system.log#
              ###########################################
           '''
  else:
     filename = sys.argv[1]
     timer(filename)


