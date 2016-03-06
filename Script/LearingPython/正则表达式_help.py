#!/usr/bin/env python
#__*__ coding: utf-8 _*_

import os,re

#正则表达式的用法
#p = re.compile(r"")

###################################################
#读取文件内容
#让文件内容逐行的输出到屏幕
def file_print():
   #切换到指定目录
   os.chdir("/var/log")
   for f in open("/var/log/system.log"):
     print f
#####################################################
# 提示系统日志(system.log) 分为八个部分 1.月 2.日期 3.时间
# 4. 用户 5.进程名[id] 6.动作（进程做啥了） 7. 状态（err） 8.内容提要
def re_grep():
   #使用re.compile编译可以提高效率
   ############################################################
   #########################################
   ## 匹配包含“kernel [0]:”内容，并且把所在的行打印出来
   ## p = re.compile(r"\w+\s.+\s+(kernel\[0\]:)+\s+\w.*")
   ## 匹配包含“err或error”内容，并且把所在行打印出来(不包含中文)
   ## p = re.compile(r"\w+\s.+\s+(erro?r?)+\s.+\w+(.*?)")
   ###################################################
   ##############################################################
   
   # One:
   #================================================= 
   # p = re.compile(r"\w+(error|err)") #以下是过滤结果
   # ml_get_interr
   # OS_xpc_error
   # interr
   # ml_get_interr
   # ml_get_interr
   # ml_get_interr
   # ml_get_interr
   # connectionWithClientInterr
   # ml_get_interr
   # ml_get_interr
   #==============================================================
   # Two:
   # p = re.compile(r"\w+\s.+(error|err)") #以下是过滤结果
   # Sep 15 04:55:45 yangjunfei mDNSResponderHelper[6527]: do_mDNSInterfaceAdvtIoctl: ioctl call SIOCGIFINFO_IN6 failed - error
   # Sep 15 04:55:47 yangjunfei CalendarAgent[219]: [com.apple.calendar.store.log.caldav.queue] [Account refresh failed with error
   # Sep 15 04:55:54 yangjunfei mDNSResponderHelper[6527]: do_mDNSInterfaceAdvtIoctl: ioctl call SIOCGIFINFO_IN6 failed - error
   # 以上是过滤的一部分，其余省略。把全部200行都过滤出来了。只是err后面的还没出来    
   #==================================================================
   # Three:
   p = re.compile(r"\w+\s.+(error|err)+\s.+\w+\D+") #以下是过滤结果
   #for t in open("/var/log/system.log"):
   for t in open("/tmp/err.log"):
     S = p.search(t)
     try:
      if S  :
        print   S.group(0)
        #if S.group(0) is "":
        # print '''\033[34m ================\n
        #           没有内容与之匹配,请检查正则表达
        #         ==========================\033[0m\n
        #       '''
        
     except: 
        print ''' \033[34m ====== 开始=========\n
                    匹配失败.....
              ==========================\033[0m\n
              '''
        
 ######
# \s 匹配所有“空白”(\s*)； \S 除\s之外； \w 匹配 [a-zA-Z0-9] 在[\w+ 很有用，可以用来匹配一个单词]；
# \W 除\w之外；\d [0-9] ; \D 除\d之外； (.*) /i 忽略大小写；
#正在表达式的注意：
# \w+ (匹配文本) ；
# \s. ("." 特殊字符完全匹配任何字符,包括换行;没有这个标志, "." 匹配除了换行外的任何字符。[\s.全部分隔符])
# .*? (任意文本，也可为空)
# .? (匹配一个肯出现的空格)
# \s*(Skip leading whitespace 忽略空白)。
# ?(例子："July|Jul" 使用"July?"也可以替代)
if __name__ == '__main__':
    #file_print()
    re_grep()
