# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: yangjunfei2146@gmail.com
#  File Name: ceph_swift_tool
#  Description:
#  Edit History: 2015-12-16
# ==================================================
import sys,os
from functools import  wraps
try:
    import swiftclient
except:
    print("loading swiftclient mode failed, process will exit....")
    sys.exit(1)

def action_ceph_do(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        tmp = func(*args,**kwargs)
        # print tmp
        user = tmp[0]
        key = tmp[1]
        authurl = tmp[2]
        container_name = tmp[3]
        object_name = tmp[4]
        action = tmp[5]
        try:
            conn = swiftclient.Connection(
                user=user,
                key=key,
                authurl=authurl,
            )
            print("connection %s success...." % authurl)
        except:
            print("connection %s failed...." % authurl)
        #print action,"aaaaaaa"
        if action == "create_container":
            # create a container
            try:
                conn.put_container(container_name)
                print("Container %s to create success...." % container_name)
            except:
                print("Container %s to create failed...." % container_name)
        elif action == "create_object":
            # create an object
            try:
                with open(object_name,'r') as f:
                    conn.put_object(container_name,object_name,
                                    contents=f.read())
                                    #content_type='text/plain')
                                    #content_type='binary/octet-stream')
                print("Object %s to create success...." % object_name)
            except:
                print("Object %s to create failed...." % object_name)
        elif action == "list_containers":
            # list owned containers
            try:
                for container in conn.get_account()[1]:
                    print container['name']
            except:
                print("Container list failed.....")
        elif action == "show_container_content":
            # list a container's content
            try:
                for data in conn.get_container(container_name)[1]:
                    print '{0}\t{1}\t{2}'.format(data['name'],data['bytes'],data['last_modified'])
            except:
                print("show %s container failed..." % container_name)
        elif action == "downlaod_object":
            # download an object
            try:
                obj_tupe = conn.get_object(container_name,object_name)
                if '/' in object_name:
                    object_file=object_name.split('/')[-1]
                    path_num=int(len(object_name.split('/'))-1)
                    #print path_num
                    for i in xrange(path_num):
                        if not os.path.exists(object_name.split('/')[i]):
                                os.makedirs(object_name.split('/')[i],0o755)
                                print i
                        os.chdir(object_name.split('/')[i])
                        print "cd is dir is %s" % object_name.split('/')[i]
                    with open(object_file,'wb') as f:
                        f.writelines(obj_tupe[1])
                    print("Download %s success...." % object_name)
                else:
                    with open(object_name,'wb') as f:
                        f.writelines(obj_tupe[1])
                    print("Download %s success...." % object_name)
            except:
                print("Download %s failed...." % object_name)
        elif action == "delete_object":
            # Delete an object
            try:
                conn.delete_object(container_name,object_name)
                print("Delete %s success..." % object_name)
            except:
                print("Delete %s failed..." % object_name)
        elif action == "delete_container":
            # Delete an container
            try:
                conn.delete_container(container_name)
                print("Delete %s success..." % container_name)
            except:
                print("Delete %s failed [Note: The container must be "
                      "empty!Otherwise the requst won't work]..." % container_name)
        return tmp
    return wrapper


class ceph:
    @action_ceph_do
    def create_container(self,user,key,authurl,container_name,object_name=None,
                                  action="create_container"):
        return (user,key,authurl,container_name,
                object_name,action)
    @action_ceph_do
    def create_object(self,user,key,authurl,container_name,
                                object_name,action = "create_object"):
        return (user,key,authurl,container_name,
                object_name,action)
    @action_ceph_do
    def list_containers(self,user,key,authurl,
                                    container_name,object_name,
                                    action="list_containers"):
        return (user,key,authurl,container_name,
                object_name,action)
    @action_ceph_do
    def show_container_content(self,user,key,authurl,container_name,
                                        object_name=None,
                                        action="show_container_content"):
        return (user,key,authurl,container_name,
               object_name,action)
    @action_ceph_do
    def download_object(self,user,key,authurl,container_name,
                                  object_name,action="downlaod_object"):
        return (user,key,authurl,container_name,object_name,action)
    @action_ceph_do
    def  delete_object(self,user,key,authurl,container_name,
                            object_name,action="delete_object"):
        return (user,key,authurl,container_name,
               object_name,action)
    @action_ceph_do
    def delete_container(self,user,key,authurl,container_name,
                             object_name=None,action="delete_container"):
        return (user,key,authurl,container_name,
                object_name,action)
def usage():
    usages='''
precondition:
    configure user,key,authurl for ceph_swift_tool;
    example:
    def __init__(self):
        self.user = 'test:swift'
        self.key = '3YAbLcxCLLQpEsChAIYDepBUTq3y006K43aYmGem'
        self.authurl = 'http://monosd01/auth/1.0'
Usage:
    python ceph_swift_tool.py [option <create|upload|delete|list|download>] [contianer <contianer name>] [object <object name>]
Example:
    # create contianer
    python ceph_swift_tool.py  create kycloud
    # list  contianer
    python ceph_swift_tool.py  list
    # delete an contianer
    python ceph_swift_tool.py  delete kycloud
    # upload object in kycloud contianer
    python ceph_swift_tool.py  create|upload kycloud kycloud_file
    # list a container's content
    python ceph_swift_tool.py  list kycloud
    # download an object
    python ceph_swift_tool.py  download kycloud kycloud_file
    # delete an object
    python ceph_swift_tool.py  delete kycloud kycloud_file
    '''
    print usages

if __name__ == '__main__':
    user = 'test:swift'
    key = '3YAbLcxCLLQpEsChAIYDepBUTq3y006K43aYmGem'
    authurl = 'http://monosd01/auth/1.0'
    #action = None
    if len(sys.argv) == 3:
        container_name = sys.argv[2]
        #object_name = sys.argb[3]
        container_cmd = sys.argv[1]
        #print container_cmd
        do = ceph()
        if container_cmd == "create":
            do.create_container(user,key,authurl,container_name,None)
        elif container_cmd == "list":
            do.show_container_content(user,key,authurl,container_name,None)
        elif container_cmd == "delete":
            do.delete_container(user,key,authurl,container_name,None)
    elif len(sys.argv) == 4:
        object_cmd = sys.argv[1]
        container_name = sys.argv[2]
        object_name = sys.argv[3]
        #print object_cmd
        do = ceph()
        if object_cmd == "upload" or object_cmd == "create":
            do.create_object(user,key,authurl,container_name,object_name)
        elif object_cmd == "download":
            do.download_object(user,key,authurl,container_name,object_name)
        elif object_cmd == "delete":
            do.delete_object(user,key,authurl,container_name,object_name)
        else:
            usage()
    elif len(sys.argv) == 2:
        option = sys.argv[1]
        print option
        if option == '-v' or option == '--version':
            print('0.1 beta')
        elif option == "list":
            do = ceph()
            container_name = None
            do.list_containers(user,key,authurl,container_name,None)
        else:
            usage()

    else:
        usage()


