#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os,time
import sys,traceback
import socket
from otomat.conf import conf


class active_server:
    def __init__(self,filename=None):
        self.filename = filename
        cnf = conf.files_conf_check(self.filename)
        self.port = cnf.server_port() 
        self.ip =  cnf.server_ip()

    def server_receive(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((self.ip,int(self.port)))
        s.listen(9)
        try:
            while True:
                try:
                    clientconn,clientaddr=s.accept()
                except (KeyboardInterrupt, SystemExit):
                    #print "you have CTRL+C,Now quit"
                    raise
                except:
                    traceback.print_exc()
                    continue
                '''
                注：服务器端一次只接收8092个字节的数据，我让读取进入循环，
                '''
                # Process the connection
                try:
                    print "Got connection form", clientconn.getpeername() 
                    while True:
                        #data2=''
                        data=clientconn.recv(1024)
                        if not len(data):
                            clientconn.send('welcome',data)
                            break
                        clientconn.sendall(data)
                        data += data
                        print data 
                except (KeyboardInterrupt, SystemExit):
                    #print "you have CTRL+C,Now quit"
                    raise
                except:
                    traceback.print_exc()
                # Close the connection
                try:
                    clientconn.close()
                except KeyboardInterrupt:
                    raise
                except:
                    traceback.print_exc()

        except (KeyboardInterrupt, SystemExit):
            print "you have CTRL+C,Now quit"
            raise
        except:
            traceback.print_exc()
        finally:
            s.close()

def main(f):
    t =  active_server(f)
    t.server_receive()
if __name__ == "__main__":
    main("otomat.cnf")
