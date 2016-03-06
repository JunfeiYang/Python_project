#usr/bin/env python
#coding=utf8

import threading,subprocess,time


def shell_cmd(cmd):
        subprocess.PIPE
        #cmd = 'ping -c %s %s' % (3,"baidu.com"+"\n")
        PING  = subprocess.Popen(cmd,stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                shell=True)
        PING.stdin.close()
        PING.wait()
        print "execution result: %s" % PING.stdout.read()

def thread_check(cmd):
        threadname = threading.currentThread().getName()
        shell_cmd(cmd)

def main():
        cmd_list = []
        threads = []
        address_list = ["a.com","b.com,","c.com","d.com","e.com","f.org","g.com"]
        for address in address_list:
                cmd = 'ping -c %s -i 0.1 %s' % (3,address+"\n")
                threads.append(threading.Thread(target=thread_check(cmd),))
        for t in threads:
                t.setDaemon(1)
        for t in threads:
                t.start()
                time.sleep(0.1)
        for t in threads:
                t.join()
        

if __name__ == "__main__":
        main()
