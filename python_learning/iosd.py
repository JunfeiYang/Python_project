#!/usr/bin/python
#coding=utf-8
import sys
import os
import commands
import re
import json
################################################################
Commond_Ceph_getOsdDelay="ceph osd perf";
Ceph_OSDID="OSDID";
def readShell(cmd):
   ret1, ret2 = commands.getstatusoutput('ceph osd perf');
   ##ret1=0;
   ##ret2="abc";
   return ret1,ret2;

class OsdDelay:
   __len=0;
   __flag=False;
   __osdDict = {};
   def __init__(self, content ):
       self.content = content;
       self.__len=len(self.content);
       if self.__len > 0:
          strrows = self.content.split('\n');  ## get every line
          tmplen = len(strrows);
	  tmpkey="";
	  ##print("tmplen=",tmplen);
          for index in range(0, tmplen):
             strcols = re.split(r' \s+', strrows[index].strip());
             ##print("index=",strcols[0]);
	     ##strcols = re.split(' ', strrows[index]);
             tmpkey=""+strcols[0]+"";
             if not strcols[0].startswith('osd'):
                self.__osdDict[tmpkey]=strrows[index];
                self.__flag=True;
             ##else:
                ##print(strcols[0]);
                ##print("length=%s" % len(strlines));## how many line

   def showData(self):
      if self.__flag:
         tmplen = len(self.__osdDict);
         ##for index in range(0, tmplen):
         ##print("dict len=%s" % tmplen);
         ##print(self.__osdDict);
      else:
         print("temp",self.__flag);

   def getCommitValue(self,id):
      sret="null";
      if self.__flag:
         cur_row=self.__osdDict.get(id);
         ##print("cur_row%s" % cur_row);
         if cur_row !=None:
         	strcols = re.split(r' \s+', cur_row.strip());
         	##strcols = re.split(' ', cur_row.strip());
         	sret=strcols[1];
      return sret;

   def getApplyValue(self, id):
      sret ="null";
      if self.__flag:
         cur_row = self.__osdDict.get(id);
	 if cur_row !=None:
	 	strcols = re.split(r' \s+', cur_row.strip());
         	##strcols = re.split(' ', cur_row);
         	sret = strcols[2];
      return sret;

##{"data":[{"{#OSDID}":"65"},{"{#OSDID}":"66"}]}
   def getOsdMap(self):
      count=0;
      keyvalue="";
      dot="";
      for key in self.__osdDict:
         ##print "self.__osdDict[%s]=" % key,key;
	 ## {"{#OSDID}":"55"},
         keyvalue=keyvalue+dot+"{\"{#"+Ceph_OSDID+"}\":\""+key.strip()+"\"}";
         dot=", \n";
         count=count+1;
      if count>0:
         enddict={};
         keyvalue="{\n\"data\":[\n" +keyvalue+" ] \n} ";
         ##enddict["data"]=keyvalue;
         ##print(keyvalue);
	 return keyvalue;
         ##print("keyvalue=",keyvalue);
         ##retdict={};
         ##strs = self.content.split('\n');
################################################################
argslen=len(sys.argv);## args length
return_code,return_result=readShell(Commond_Ceph_getOsdDelay);
if return_code==0:
   ##myosd=OsdDelay("osd 01 02\nline1 11 12\nline2 21 22\nline3 31 32");
   myosd = OsdDelay(return_result);
   myosd.showData();
   ##print("get line2 commit value=%s" % myosd.getCommitValue("line1"));
   ##print("get line2 commit value=%s" % myosd.getApplyValue("line2"));
   strRet="null";
   if argslen>2:
	vid=sys.argv[1];
        vty=sys.argv[2];
	##print("vid=%s" % vid);
	##print("vty=%s" % vty);
        if vty=="commit":
	     strRet=myosd.getCommitValue(vid);
	elif vty=="apply":
	     strRet=myosd.getApplyValue(vid);            	
   else:
	tmp=myosd.getOsdMap();
	jsonRet = tmp; ##json.dumps(tmp);
	print(jsonRet);
	##print("{\n\"data\":[\n{\"{#OSDID}\": \"30\"}]\n}");
else:
   print("nono");
if not strRet=="null":
   print(strRet);