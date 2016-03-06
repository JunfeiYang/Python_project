# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: yangjunfei2146@gmail.com
#  File Name:
#  Description:
#  Edit History:
# ==================================================
import time
import  string
import sys,os
from random import choice
from logs import log as logging

reload(sys)
sys.setdefaultencoding('utf8')

home_path = os.getcwd()

logfile = 'python_IO_Test.log'
logdir = '/var/log'
if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)
os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a',limit = 102400)

os.chdir(home_path)


def io_generate_name(chars=string.letters+string.digits):
    return ''.join([choice(chars) for i in xrange(16)])

def io_genterate(func):
    path='/file_IO_test/'
    def inner(args):
        temp = func(args)
        file_name=path+io_generate_name()
        if temp == '4k':
            try:
                print "生成文件为:%s 大小为:4k" % file_name
                logging.info("生成文件为:%s 大小为:4k" % file_name)
                with open(file_name+'_4k','wb') as f:
                    f.write(os.urandom(1024*4))
            except IOError:
                print "写入4k文件失败"
                logging.error("写入4k文件失败")
                return  4
        elif temp == '1m':
            try:
                print "生成文件为:%s 大小为:1m" % file_name
                logging.info("生成文件为:%s 大小为:1m" % file_name)
                with open(file_name+'_1m','wb') as f:
                    f.write(os.urandom(1024*1024))
            except IOError:
                print "写入1m文件失败"
                logging.error( "写入1m文件失败")
                return  1000
        elif temp == '10m':
            try:
                print "生成文件为:%s 大小为:10m" % file_name
                logging.info("生成文件为:%s 大小为:10m" % file_name)
                with open(file_name+'_10m','wb') as f:
                    f.write(os.urandom(1024*1024*10))
            except IOError:
                print "写入10m文件失败"
                logging.error("写入10m文件失败")
                return  10000
        else:
            print "请输入写入的文件大小...<4k|1m|10m>"
            logging.warning("请输入写入的文件大小...<4k|1m|10m>")
        return  temp
    return inner

@io_genterate
def io_test(args):
    return args

def usage():
    usages='''
Usage:
    python Python_IO_Test.py (size 4k|1m|10m) [time number<default 1 minute>]
Example:
    python Python_IO_Test.py  4k   60
    python Python_IO_Test.py  4k
    '''
    print usages,


if __name__ == '__main__':
    start = int(time.time()) # time is 1 sec
    if len(sys.argv) == 2:
        while True:
            end = int(time.time())
            print sys.argv[1]
            if (end-start) <= 60:
                print '--------test-------'
                io_test(str(sys.argv[1]))
                print (end-start)
                print '--------test-------'
                time.sleep(0.1)
            else:
                break
    elif len(sys.argv) == 3:
        input_time = int(sys.argv[2])
        while True:
            print sys.argv[1]
            print input_time
            end = int(time.time())
            if (end-start) <= input_time:
                print '--------test-------'
                io_test(str(sys.argv[1]))
                print (end-start)
                print '--------test-------'
                time.sleep(0.1)
            else:
                break
    else:
        usage()
