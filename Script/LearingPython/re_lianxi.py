#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
import re
import string
#
#
s = ('xxx','abcxxxabc','xyx','abc','x.x','axa','axxxxa','axxya')
###########################################################
#                                                         #
# 这个练习的想法是能够将正则表达式应用到不同的字符串来确定# 
# 哪些与其匹配，哪些不匹配。要在输入的一行中完成工作，可以#
# 使用filter函数，但是因为filter函数，对于其输入列表的每个#
# 成员应用带有一个参数的函数，而re.match和re.search有两个参#
# 数，所以您不得不使用函数定义或者lambda形式(如本例所式)  #
# #########################################################


# 1
a = filter((lambda s: re.match(r"xxx",s)),s)
print "这是测试a：%s" % a
# xxx
# 为什么输出结果是xxx，因为re.match函数只从它输入开始匹配搜索。
# 要在输入的任何地方找到可以采用re.search

# 2
b = str(filter((lambda s: re.search(r"xxx",s)),s))
#print  b
print "这是测试b：%s" % b
# 3
c = str(filter((lambda s: re.search(r"x\.x",s)),s))
print "这是测试c：%s" % c
# 4
d = str(filter((lambda s: re.search(r"x.*x",s)),s))
print "这是测试d：%s" % d
# 5
#匹配任意数量的x
e =str(filter((lambda s: re.search(r"x.*x",s)),s))
"这是测试e：%s" % e
#6
#确保两个x之间有字符，+匹配一个或多个字符
f = str(filter((lambda s: re.search(r"x.+x",s)),s))
print "这是测试f：%s" % f
#7
#匹配没有c的任何字符
g = str(filter((lambda s: re.search(r"[^c]*",s)),s))
print "这是测试g：%s" % g
#8
#匹配'c,cc,ccx'
h = str(filter((lambda s: re.search(r"[^c]*",s)),('c','cc','ccx')))
print "这是测试h：%s" % h
#9
i = str(filter((lambda s: re.search(r"^[^c]*$",s)),s))
print "这是测试i：%s" % i
# “.*?”匹配所有字符，包括空白。

