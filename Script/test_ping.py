#!/usr/bin/env python
# -*- coding: utf8 -*-
import subprocess
import re
import time
import os
lost_rate_match = re.compile('(\d+)\spackets transmitted, (\d+)\sreceived,\s(\d+(.\d+)?%)')
time_match = re.compile('(?P<min>\d+.\d+)\/(?P<avg>\d+.\d+)\/(?P<max>\d+.\d+)\/(?P<mdev>\d+.\d+)')
#pre_fix = os.sys.path[0]
pre_fix = "/Users/yangjunfei/Documents/Python/Script"
class PingTest(object):

    def __init__(self, ip, count=100, psize=False, writelog=True):
        """默认一次ping一百个数据包，包大小为系统默认，同时不输出到屏幕，结果输出到日志文件"""
        self.record_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self._runping(ip, count, psize, writelog)

    def _getping(self, ip, count, psize):
        """使用subprocess获取ping测试的原始结果，count为ping的次数，psize为ping包大小"""
        if psize:
            if isinstance(psize, int):
                if psize > 0 and psize <= 65507:
                    ping_command = 'ping -c %s -s %s %s' %(count, psize, ip)
                else:
                    return 2
            else:
                return 1
        else:
            ping_command = 'ping -c %s %s' % (count, ip)
        ping = subprocess.Popen(ping_command,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
        return ping.stdout.read()

    def _runping(self, ip, count, psize, writelog):
        """主函数，调用_getping获取原始数据并做一定的格式处理，同时可选择记录到日志中"""
        ping_ori_result = self._getping(ip, count, psize)
        if ping_ori_result == 1:
            print 'psize must be <int> type'
            return 0
        if ping_ori_result == 2:
            print 'packet size 65527 is too large. Maximum is 65507'
            return 0
        data_format = self._format(self._getresult(ping_ori_result))
        if writelog:
            if self._writelog(ip, data_format):
                return 1
            else:
                return 0
        else:
            print data_format

    def _writelog(self, ip, result):
        """将结果记录到日志中，位置为脚本所在目录的logs目录"""
        filename = '%s/logs/%s.log' %(pre_fix, ip)
        try:
            f = open(filename, 'a')
        except IOError, e:
            print e
            return 0
        f.write('%s\n' % result)
        f.close()
        return 1

    def _getresult(self, context):
        """从原始数据中或许丢包率和ping包返回时间"""
        lost_rate = lost_rate_match.findall(context)
        time_result = time_match.findall(context)
        return (lost_rate,time_result)

    def _format(self, rawdata):
        """将数据排列成一定的格式"""
        (lostrate, time_result) = rawdata
        if time_result:
            time_context = ' / '.join(time_result[0])
        else:
            time_context = 'null'
        return '[%s] total: %s received: %s lost: %s time: %s' % (self.record_time, lostrate[0][0], lostrate[0][1], lostrate[0][2],time_context)

if __name__ == '__main__':
    from multiprocessing import Pool
    import os
    iplist = '%s/ip.list' % pre_fix
    if os.path.exists(iplist):
        p = Pool(100)
        p.map(PingTest, filter(None ,[x.strip() for x in open(iplist, 'r').readlines()]))
    else:
        print 'Not Found %s' % iplist


