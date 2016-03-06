#!/usr/bin/env python
# -*- coding: utf8 -*-
import re

log_path = '/tmp/ping_analysis/logs_BJ/logs/'

result_sets = {}
date_format = re.compile('(\d{4}-\d{2}-\d{2}\s\d{2}).*')

"""获取ip对应城市和线路信息并生成字典
   原始文件格式为ip地址\t城市\t线路，如：202.96.209.133\t上海\t中国电信
   生成字典格式为 ip地址：ip地址(城市/线路)，如：{'202.96.209.133':'202.96.209.133(上海/中国电信)'}
"""
ip_city = {}
map(lambda x : ip_city.update({x[0]:'%s(%s/%s)'%(x[0],x[1],x[2])}), map(lambda x: x.strip().split('\t'), open('/tmp/ping_analysis/ip_city_op.txt').readlines()))

def processdata(ori_data):
    """按照date_format的格式统计数据"""
    datetime = ori_data[0].strip()
    ping_lost = float(ori_data[1].strip())
    if ori_data[2].strip() == 'null':
        ping_min = 0.0
        ping_avg = 0.0
        ping_max = 0.0
    else:
        ping_min = float(ori_data[2].strip())
        ping_avg = float(ori_data[3].strip())
        ping_max = float(ori_data[4].strip())
    datetime_key = date_format.match(datetime).group(1)
    if datetime_key in result_sets:
        result_sets[datetime_key]['total_lost'] = result_sets[datetime_key].get('total_lost') + ping_lost
        result_sets[datetime_key]['total_min'] = result_sets[datetime_key].get('total_min') + ping_min
        result_sets[datetime_key]['total_avg'] = result_sets[datetime_key].get('total_avg') + ping_avg
        result_sets[datetime_key]['total_max'] = result_sets[datetime_key].get('total_max') + ping_max
        result_sets[datetime_key]['lost_count'] = result_sets[datetime_key].get('lost_count') + 1
        if ping_min:
            result_sets[datetime_key]['time_count'] = result_sets[datetime_key].get('time_count') + 1
    else:
        result_sets[datetime_key] = {}
        result_sets[datetime_key]['total_lost'] = ping_lost
        result_sets[datetime_key]['total_min'] = ping_min
        result_sets[datetime_key]['total_avg'] = ping_avg
        result_sets[datetime_key]['total_max'] =  ping_max
        result_sets[datetime_key]['lost_count'] = 1
        if ping_min:
            result_sets[datetime_key]['time_count'] = 1
        else:
            result_sets[datetime_key]['time_count'] = 0

def data_format(fp=0):
    """processdata处理完数据后进行平均值的计算并写入指定文件"""
    items = result_sets.keys()
    items.sort()
    for item in items:
        lost_count = result_sets[item].get('lost_count')
        time_count = result_sets[item].get('time_count')
        avg_lost = round(result_sets[item].get('total_lost') / lost_count, 4)
        try:
            avg_min = round(result_sets[item].get('total_min') / time_count, 4)
            avg_avg = round(result_sets[item].get('total_avg') / time_count, 4)
            avg_max = round(result_sets[item].get('total_max') / time_count, 4)
        except ZeroDivisionError:
            avg_min = avg_avg = avg_max = 'null'
        if fp:
            fp.write('\t%s\t%s%s\t%s\t%s\t%s\n' % (item, avg_lost, chr(37), avg_min, avg_avg, avg_max))

def originaldata(items, fp=0):
    """不运行processdata直接将数据输出到指定文件"""
    for item in items:
        if fp:
            if item[2] == 'null':
                fp.write('\t%s\t%s%s\t%s\t%s\t%s\n' % (item[0], item[1], chr(37), item[2], '', ''))
            else:
                fp.write('\t%s\t%s%s\t%s\t%s\t%s\n' % (item[0], item[1], chr(37), item[2], item[3], item[4]))

def runprocess(original_data, fp=0, start_date=0, hourly=True):
    """主函数"""
    def middleprocess(original_data, start):
        """将原始数据分割，并可按开始时间记录数量"""
        middle_result = []
        middle_temp = map(lambda x: tuple(x.strip().split(',')),original_data)
        if start_date:
            for handle in middle_temp:
                if handle[0] >= start:
                    middle_result.append(handle)
            return middle_result
        else:
            return middle_temp
    if hourly:
        """数据是否要经过processdata的处理"""
        map(processdata, middleprocess(original_data, start_date))
        return data_format(fp)
    else:
        originaldata(middleprocess(original_data, start_date), fp)

def file_format(filename):
    """读取日志文件，并对每一行做格式化处理：去除[,],%以方便后续的计算"""
    context = filter(None, map(lambda x: x.strip().split(), open(filename, 'r').readlines()))
    def format_data(line):
        if line[9].strip() == 'null':
            time_line = 'null'
        else:
            time_line = '%s,%s,%s' % (line[9], line[11], line[13])
        return '%s %s,%s,%s' % (line[0].strip('[ '),line[1].strip('] '), line[7].strip('% '), time_line)
    return map(format_data, context)



if __name__ == '__main__':
    import os
    result_log = open('%s%s' %(log_path,'result_log.xls'), 'w')
    for dirpath, dirnames, filenames in os.walk(log_path):
        print dirpath
        for filename in filenames:
            if filename.endswith('.log'):
                result_log.write('%s\n' % ip_city.get(filename.strip('.log')))
                runprocess(file_format('%s%s' % (log_path, filename)), result_log, start_date='2011-03-24 18:00:00', hourly=False)
    result_log.close()

