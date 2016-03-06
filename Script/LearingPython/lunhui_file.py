#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os,sys,shutil

path=sys.argv[1]
#print path
#
def make_version_path(path,version):
    if version == 0:
       #NO suffix for version 0, the current version
       return path
    else:
       #Append a suffix to indicate the older version
       return path + "." + str(version)
#print "'%s' is ok" % make_version_path(path,version=0)
#
def rotate(path,version=0):
    #Construct the name of the verison we're rotating .
    old_path = make_version_path(path,version)
    #print old_path
    if not os.path.exists(old_path):
       #It doesn't exist,so compain.
       raise IOError("'%s' does not exist" % path)
    #Construct the new version name of this file.
    new_path = make_version_path(path,version + 1)
    #Is there already a version with this name ?
    if os.path.exists(new_path):
       #Yes,Rotate it out of the way first !
       rotate(path,version + 1)
    #Now we can rename the version safely
    shutil.move(old_path,new_path)

#print "'%s' is ok" % rotate(path,version=0)
#
def rotate_log_file(path):
    if not os.path.exists(path):
       #The file is missing,so create it.
       new_file = file(path,"w")
       #Close the new file immediately ,which leaves it empty.
       del new_file
    #Now, roate it.
    rotate(path)


###
if __name__ == '__main__':
     if len(sys.argv) > 2:
        print "Usage: ", sys.argv[0] ," [path/file]   "
        print  "ex: ", sys.argv[0],"/tmp/test"
     if len(sys.argv) == 2:
        name=sys.argv[1]
       # print "现在开始轮回 %s %s" % (name,rotate_log_file(sys.argv[1]))
        print "现在开始轮回  %s" % (rotate_log_file(sys.argv[1]))
        print "轮回结束，收工"
