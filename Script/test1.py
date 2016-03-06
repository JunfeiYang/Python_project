#!/usr/bin/python
#========================================================================
# Author:Junfei Yang
# Email:yangjunfei2146@gmail.com
# File Name: test1.sh
# Description:  
# The functionality of this script is to allow the user to enter two numbe#-rs A and B , and then calculate the aggregate has been added to B from A# plus
# Edit History:
#2012-09-27 File created.
#========================================================================
numb1 = int(raw_input("Please input the first int number: "))
numb2 = int(raw_input("Please input the second int number: "))
sum = 0
for i in range(numb1,numb2+1):
 sum = sum + i
 print ('The sum of %d ~ %d = %d' % (numb1,numb2,sum))
 print ("Done!!")
 
