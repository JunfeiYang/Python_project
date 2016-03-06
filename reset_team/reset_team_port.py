#!/bash/env python

import pexpect as expect
import sys,time,os
import subprocess

from logs import log as logging

logfile='reset_team_port.log'
logdir='/var/log'
if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)
os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')


def shell_cmd(cmd):
    	subprocess.PIPE
	#cmd= 'ping -c %s -i %s %s' % (3,0.01, "172.16.205."+str(i)+"\n")
	P=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                     stdout = subprocess.PIPE,
                     stderr = subprocess.PIPE,
                     shell = True)
	P.stdin.close()
	P.wait()
	return  P.stdout.readlines()


def rest_team_port(port):
    user = 'wangpeng'
    ip = '192.168.205.3'
    passwd='1haoche@151111!'
    
    # logging in switch
    child = expect.spawn('telnet %s' %ip)
    index = child.expect('User:')
    if (index != 0):
        print "faild logging the switch..."
        logging.error("faild logging the switch...")
	child.close(force=True)
    else:
        try:
            child.sendline(user)
            print 'user:',user
            logging.info('user:%s' %user)
            child.expect('Password:')
            child.sendline(passwd)
            print 'passwd:',passwd

            # rest port status
            child.expect('>')
            child.sendline('en')
            #
            child.expect('#')
            child.sendline('conf t')
            #
            child.expect('\(config\)#')
            child.sendline('interface port-channel %s' %port)
            #
            child.expect('\(config-if-Po%s\)#' %port)
            child.sendline('shut')
            child.expect('\(config-if-Po%s\)#' %port)
            child.sendline('no shut')
            print 'port:',port
            logging.info('port:%s' %port)
            #
            child.expect('\(config-if-Po%s\)#' %port)
            child.sendline('do show interface port-channel')

            print child.before
        except:
            traceback.print_exc()
            logging.error("login failed....")
        finally:
             child.close(force=True) 
             logging.info("login end .......")
    
if __name__ == '__main__':
    while True:
        team0_cmd='fping 192.168.204.2'
        team0_active = shell_cmd(team0_cmd)
        team1_cmd='fping 192.168.203.2'
        team1_active = shell_cmd(team1_cmd)
        print team0_active
        print team1_active
        if 'alive' not in team0_active[0]:
	    port = '17'
            logging.debug("this is team0")
            print "this is tema0"
            rest_team_port(port)
        if 'alive' not in team1_active[0]:
	    port = '12'
            print "this is tema1"
            logging.debug("this is team0")
            rest_team_port(port)
	time.sleep(10)
	continue

		
		
