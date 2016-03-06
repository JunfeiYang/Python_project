#######################
This is Redme File .It's the main purpose the project of simple help.
The following is utf-8 format in Chinese:

============
　　主要针对壹号车OpenStack staging平台服务，现阶段主要包括两个功能，检测
平台各个租户的虚拟机的状态，平台虚拟机的启停，运硬盘的挂载和卸载．
一：平台虚拟机的启停（运硬盘的挂载和卸载）
１．首先运行环境，通过加载相关环境变量实现的会有内部与公有之分且确保url可用．
２．进入platform-manager/
    sudo python platfrom_manager.py 
    可以根据提示，操作
    sudo python platfrom_manager.py
     please use the -h or --help
    sudo python platfrom_manager.py　-h
    Usage: platfrom_manager.py [options]

    Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -a start|stop, --action=start|stop
                        Stop or start virtual machine and mount cloud devices.
3.在做１与２的事情之前，你必须配置plugins/platform_manager.conf
  格式：
    [kyprivate]
    OS_AUTH_URL=http://172.16.209.11:5000/v2.0
    OS_TENANT_ID=4d550d27d9f64c7ba2580cad4c1cfa5f
    OS_TENANT_NAME=kyprivate
    OS_USERNAME=kyprivate
    OS_PASSWORD=che001

    [kycloudprod]
    OS_AUTH_URL=http://172.16.209.11:5000/v2.0
    OS_TENANT_ID=f1134680ff48420382bad868071bb115
    OS_TENANT_NAME=kycloudprod
    OS_USERNAME=kycloudprod
    OS_PASSWORD=che001

    [kyp2p]
    OS_AUTH_URL=http://172.16.209.11:5000/v2.0
    OS_TENANT_ID=ee6e6400058a4ba3a32526de4f66c9d3
    OS_TENANT_NAME="KY_P2P"
    OS_USERNAME=kyp2p
    OS_PASSWORD=che001
4.在启动实例挂载运硬盘的同时，需要修改volume 文件的日期
    例如：
       list_openstack_volume-2015-07-31
       修改为当前日期（今天是2015-08-03）
       list_openstack_volume-2015-08-03
    文件位置在/var/lib/platform-manager/
    格式为list_ + 租户名称　＋volume-　＋日期

       
二：检测平台各个租户的虚拟机的状态
１．必须在network节点进行操作，手动添加namespace id．
    neutron router-list |grep YOURROUTRID
    ip netns list |grep YOURROUTRID
    grep namespace_id platfrom_check.py
        #namespace_id = "qrouter-368182ef-6035-46ae-8910-0b0fc0614478"
        namespace_id = "qrouter-513b894d-c157-41b9-9bd8-f35ea36114be"
        cmd_check = "ip netns exec %s fping %s" %(namespace_id,ip)
2.配置plugins/platform_check.conf，格式与plugins/platform_manager.conf相同．
3.进入platform-manager/
    sudo python  python platfrom_check.py
        Please use '-h' option.
        please use the -h or --help
    sudo python platfrom_check.py -h
    Usage: platfrom_check.py [options]

    Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -c check, --check=check
                          Check the platform so the tenant instances,running
                          state.


