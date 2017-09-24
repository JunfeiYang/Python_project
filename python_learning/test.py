__author__ = 'andre'

import time

big_month = ['1','3','5','7','8','10','12']
small_month = ['4','6','9','11']
execpt_month = ['2']

n = time.localtime(time.time())
if n.tm_mon < 10 and n.tm_mday <10:
        now = str(n.tm_year)+'-0'+str(n.tm_mon)+'-0'+str(n.tm_mday)
elif n.tm_mon < 10 and n.tm_mday >= 10:
        now = str(n.tm_year)+'-0'+str(n.tm_mon)+'-'+str(n.tm_mday)
elif n.tm_mon >= 10 and n.tm_mday <10:
        now = str(n.tm_year)+'-'+str(n.tm_mon)+'-0'+str(n.tm_mday)
elif n.tm_mon >= 10 and n.tm_mday <10:
        now = str(n.tm_year)+'-'+str(n.tm_mon)+'-0'+str(n.tm_mday)
print "what day is it taday?Today is:",now

if n.tm_mon <= 10 and n.tm_mday <=10:
    if str(n.tm_mon-1) in big_month and str(n.tm_mdy) == '1':
        yesterday = str(n.tm_year)+'-0'+str(n.tm_mon-1)+'-'+str(31)
    elif str(n.tm_mon-1) in small_month and str(n.tm_mdy) == '1':
        yesterday = str(n.tm_year)+'-0'+str(n.tm_mon-1)+'-'+str(30)
    elif str(n.tm_mon-1) in execpt_month and str(n.tm_mdy) == '1':
        if ((n.tm_year%4==0 and n.tm_year%100!=0) or (n.tm_year%400==0)):
            yesterday = str(n.tm_year)+'-0'+str(n.tm_mon-1)+'-'+str(29)
        else:
            yesterday = str(n.tm_year)+'-0'+str(n.tm_mon-1)+'-'+str(28)
    else:
        yesterday = str(n.tm_year)+'-0'+str(n.tm_mon)+'-0'+str(n.tm_mday-1)
elif  n.tm_mon <= 10 and n.tm_mday > 10:
    yesterday = str(n.tm_year)+'-0'+str(n.tm_mon)+'-'+str(n.tm_mday-1)
elif n.tm_mon >= 10 and n.tm_mday <=10:
    if str(n.tm_mon-1) in big_month and str(n.tm_mdy) == '1':
        yesterday = str(n.tm_year)+'-'+str(n.tm_mon-1)+'-'+str(31)
    elif str(n.tm_mon-1) in small_month and str(n.tm_mdy) == '1':
        yesterday = str(n.tm_year)+'-'+str(n.tm_mon-1)+'-'+str(30)
    else:
        yesterday = str(n.tm_year)+'-'+str(n.tm_mon)+'-0'+str(n.tm_mday-1)
elif n.tm_mon >= 10 and n.tm_mday <=10:
    yesterday = str(n.tm_year)+'-'+str(n.tm_mon)+'-0'+str(n.tm_mday)

print yesterday