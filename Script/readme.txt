1. tar -xvf sshmonitor.tar.gz
2. cd pycrypto-2.5
3. python setup.py install
4. cd ../paramiko-1.7.7.1
5. python setup.py install
6. cd ../sshmonitor
7. vi config
  change check property
    *_NODE=?       //为要检测的进程所在服务器列表，空格分隔，如:BITSFLOW_NODE=192.168.204.31 192.168.204.32
    *_USERS=?      //为服务器用户名，用于ssh登录要检测的节点，空格分隔，需要与BITSFLOW_NODE对应
    *_PASSWORDS=?      //为服务器密码，用于ssh登录要检测的节点，空格分隔，需要与BITSFLOW_NODE对应
    *_CHECK_PROCESS_PATH=?      //为检查进程时所使用的路径关键字，通过该路径能初步定位到路径下所有的启动进程，空格分隔，第一个可作为默认值，供所有节点使用
    *_CHECK_KEYS=?    //进一步确定进程的关键字，通常为进程名称，各节点使用|分隔，进程名称和进程数量使用:号分隔
8. 。/main.py
  correct result:
    check 192.168.204.31's agent process ok
    check 192.168.204.31's netvmd process ok
    check 192.168.204.35's agent process ok
    check 192.168.204.35's netvm process ok
    check 192.168.204.35's groupd process ok
    0 Ok
    check 192.168.204.35's DataCell process ok
    check 192.168.204.36's DataCell process ok
    check 192.168.204.37's DataCell process ok
    0 Ok
    check 192.168.204.38's tomcat process ok
    0 Ok
  failed result:
    check 192.168.204.31's agent process ok
    check 192.168.204.31's netvmd process ok
    check 192.168.204.35's agent process ok
    check 192.168.204.35's netvm process ok
    check 192.168.204.35's groupd process ok
    0 Ok
    error: not found DataCell process in 192.168.204.35
    error: not found DataCell process in 192.168.204.36
    error: not found DataCell process in 192.168.204.37
    1 Error
    check 192.168.204.38's tomcat process ok
    0 Ok
