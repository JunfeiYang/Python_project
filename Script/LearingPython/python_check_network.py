import socket
import struct
import thread
import threading
import time
import os
net_data = {}
d_net_info = {}
lock = threading.Lock()


def print_data():
    while True:
          lock.acquire()
          for key in net_data:
              print "%s %s\n"%(key, net_data[key])
          lock.release()
          time.sleep(5);
                                                            
def get_net_info():
    net_info = os.popen('netstat -nbo').readlines()
                                                                    
    for l in net_info[4:]:
        s = l.split()
        if len(s)>2:
           key = "%s %s"%(s[1],s[2])
           key2 = "%s %s"%(s[2],s[1])
        else:
           if not d_net_info.has_key(key):
              d_net_info[key] = s[0]
              d_net_info[key2] = s[0]
def get_packet():
    HOST = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((HOST, 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    net_data["unknow"] = 0
    while True:
        buf = s.recvfrom(65565)
        port = struct.unpack('HH', buf[0][20:24])
        
        src_ip = "%d.%d.%d.%d"%struct.unpack('BBBB', buf[0][12:16])
        dest_ip ="%d.%d.%d.%d"%struct.unpack('BBBB', buf[0][16:20])
        src_port = socket.htons(port[0])
        dest_port = socket.htons(port[1])
        
        data_len = len(buf[0])
        key="%s:%d %s:%d"%(src_ip,src_port,dest_ip,dest_port)
        if not d_net_info.has_key(key):
           get_net_info()
        if d_net_info.has_key(key):
           key2 ="%s %s"%(key,d_net_info[key])
           if net_data.has_key(key2):
              net_data[key2] =net_data[key2]+data_len
           else:
              net_data[key2] = data_len
          
        else:
           net_data["unknow"] =net_data["unknow"] + data_len
           
thread.start_new_thread(print_data,())
get_packet()
os.exit()
