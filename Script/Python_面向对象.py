#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#


#面向对象
class Person:
  #初始化类，构造器可以用来对对象做一些你希望的初始化
  def __init__(self,name,age,sex,job,city,asset=10000):
    #前面可以自己定义，不一定与上面一样，但是=后面必须对应
    self.Name = name
    self.Age = age
    self.Job = job
    self.City = city
    self.Asset = asset

  def tell(self):
    info = '''
     \nHello,My name is %s,I am %s years old, nice to meet you
     I am a %s work in %s . How about you ?
     ''' %(self.Name,self.Age,self.Job,self.City)
    print info
#debug
#边写边调试是一个很好的习惯。
#P = Person('Bigbroher','33','man','Senior Systems Engineer','beijing')
#P.tell()
class Love(Person):
    #子类可以继承父类（asset=10000）也可以改变（asset=12000）
    def __init__(self,name,age,sex,job,city,asset=12000):
      #代表继承上一类的参数
      Person.__init__(self,name,age,sex,job,city,asset)
    def action(self,action_type):
      print action_type
      if action_type == 'FristMet':
        #因为继承父类，方法都可以调用
        self.tell()
      if action_type == 'Match 50':
        print 'Byebye, I do not like each other'
        return 50
      if action_type == 'watch movie':
        print 'you are rich man'
#debug
P = Love('Bigbroher','33','man','Senior Systems Engineer','beijing')
P.action('Match 50')
if P.action('Match 50') == 50:
    print 'sorry you are not rich man'
    print 'I want find a rich man'
    

