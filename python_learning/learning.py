__author__ = 'andre'

#from oslo.config import cfg
'''
opts = [
    cfg.StrOpt('bind_host', default='0.0.0.0'),
    cfg.IntOpt('bind_port',default=9292)
]

CONF = cfg.CONF
CONF.register_opts(opts)
CONF(default_config_files='/tmp/glance.conf')

CONF.get('host')

import os

os.system('date')

os.path.curdir
import subprocess

def shell_cmd(cmd):
    subprocess.PIPE
    P = subprocess.Popen(cmd,stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    P.stdin.close()
    P.wait()
    return  P.stdout.readlines()

shell_cmd('date')
'''
from oslo.config import cfg

opts = [
   cfg.StrOpt(
       'host',
        default= '0.0.0.0',
        help="IP address to listen on"
   ),
    cfg.IntOpt(
        'port',
        default= 8888,
        help='Port number to listen on'
    )

]



def add_common_opts(CONF):
    CONF.register_opts(opts)

def get_bind_host(CONF):
    return CONF.get('host')
def get_bind_port(CONF):
    return CONF.get('port')

cli_opts = [
    cfg.BoolOpt(
        'verbose',
        default=False,
        help='Print more verbose output'
    ),
    cfg.BoolOpt(
        'debug',
        short='d',
        default=False,
        help='Print debugging output'
    ),
]

def add_common_opts(CONF):
    #global CONF
    CONF.register_cli_opts(cli_opts)

def main():
    CONF = cfg.CONF
    add_common_opts(CONF)
    get_bind_host(CONF)
    add_common_opts(CONF)

if __name__ == "__main__":
    main()