#_*_ coding: utf-8 _*_
#apache日志分析器
import time
import re

class Apache(object):
    #filename = 'apache.log'
    filename = 'access-2013-06-10.log'
    number = 1
    #global range means the range of the number you can enter is [0: range]
    range = 3
    linedata = []
    def show(self):
     print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
     print '>>please enter a number to start the apache log analysis                   >>' 
     print '>>1:找出同一天访问次数超过N次的IP并放到以扫描当天日期命名的文件中          >>'
     print '>>2:统计每天所有query的pv和平均pv并放到文件pv                              >>'
     print '>>3:'
     print '>>0:exit system                                                            >>'
     print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
     self.range = 3

    def input_number(self, low, up):
     try:
       self.number = input()
     except NameError:
       print '\n!!please enter an number'
       return False
     if self.number >= low and self.number <=up :
       return True
     else:
       print '\n!!please enter an number in [0:'+str(self.range)+']'
       return False

    def analysis(self):
     try:
       f=open(self.filename, 'r')
     except IOError:
       print '\n!!file %s is not exits' % apache.filename
       exit(0)
     data = f.readlines()
     for line in data:
       self.linedata.append(re.split(' ',line))
     while self.number:
       self.show()
       if not self.input_number(0, self.range):
          continue
       if self.number == 0:
          print '\n!!system exiting, byebye'
       else:
          if not self.method():
           continue
          print '\n!!finished'

    def method(self):
     if self.number == 1:
        print '\n!!please enter the number N'
        if not self.input_number(1, 1000000):
           return False
        strtime = time.strftime("%Y%m%d",time.localtime())
        f = open(strtime, 'w')
        count = {}
        for line in self.linedata:
            #iptime = re.split('/', line[3])
            iptime = re.split('/', line[2])
            temp = line[0] + iptime[0] + iptime[1] +']'
            key = hash(temp)
            if key in count:
               count[key] = [temp, count[key][2] + 1]
            else:
               count[key] = [temp, 1]
        for k, v in count.items():
            if v[1] > self.number:
             f.write('%s %s\n' % (v[0], v[1]))
        f.close()
        return True
          
     if self.number == 2:
        f = open('pv.txt', 'w')
        count = {}
        for line in self.linedata:
          timelist = re.split('/', line[3])
          iplist = re.split('\.', line[0])
          monthday = timelist[0] + timelist[1] + ']'
          ipnum = int(''.join(iplist))
                                      
          key = hash(monthday)
          if key in count:
             count[key][1] = count[key][1] + 1
             count[key][2].add(ipnum)
          else:
             ipset=set()
             ipset.add(ipnum)
             count[key] = [monthday, 1, ipset]
        
        for k, v in count.items():
          f.write('%s %s %s\n' %(v[0], v[1], float(v[1]) / len(v[2])))
        f.close()

if __name__ == '__main__':
   apache = Apache()
   apache.analysis()
#=======================================================================
# 最后很多分析工作可以结合shell命令来做比如：

# 问题1：在apachelog中找出访问次数最多的10个IP。
# awk '{print $1}' apache.log |sort |uniq -c|sort -nr|head
# 问题2：在apache日志中找出访问次数最多的几个分钟。
# awk '{print $4}' apache.log |awk -F"/" '{print $3}'|cut -c 6-10|sort|uniq -c|sort -nr|head
# 问题3：在apache日志中找到访问最多的页面：
# awk '{print $7}' apache.log|sort|uniq -c|sort -nr|head
# 问题4：分析日志查看当天的ip连接数
# grep '22/Jun/2012' apache.log| awk '{print $1}' |wc -l
# 问题5：查看指定的ip在当天究竟访问了什么urlgrep '^97.83.32.128.*22/Jun/2012' apache.log| awk '{print $7}'
# 用apache日志生成器生成日志后 就可以直接使用上面的命令了
# 分析apache日志还是很有用的，可惜我的数据是随机生成的，很多规律都无法模拟
#========================================================================
