#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#========================================================================
# Author:Andre
# Email:yangjunfei2146@gmail.com
# File Name: 
# Description:
# Edit History:
# 2015-05-25 File created.
#========================================================================
import sys
import os
import config
import env_set
reload(sys)
sys.setdefaultencoding('utf8')

conf = config.tenant_conf('platform_check.conf')

def env_set_func(tenant_name):
        TENANT_NAME_LIST = conf.tenant_name()
        LEN_TENANT_NUM = len(TENANT_NAME_LIST)
        # ['kyprivate', 'kycloudprod']
        rescoure = conf.tenant_rescoure()
        # 10
        len_rescore = len(rescoure)
        r'''
    　　下面的TENANT_NAME_LIST代表有几个租户，例如：['kyprivate', 'kycloudprod']，
        len(TENANT_NAME_LIST)=2。通过for循环range(2),suffix进行组合，例如：suffix =2*5,
        url_key = rescoure[10][1]取得（http://172.16.209.11:5000/v2.0）
        '''
        for n in range(LEN_TENANT_NUM):
                if tenant_name == TENANT_NAME_LIST[n]:
                        suffix = n*5
                        url_key = rescoure[suffix][1]
                        tenant_id_key = rescoure[suffix+1][1]
                        user_name_key = rescoure[suffix+2][1]
                        password_key = rescoure[suffix+3][1]
                        tenant_name_key = rescoure[suffix+4][1]
                        env_dist = {
                                #'OS_AUTH_URL':'http://172.16.209.11:5000/v2.0',
                                'OS_AUTH_URL':url_key,
                                #'OS_TENANT_ID':'f1134680ff48420382bad868071bb115',
                                'OS_TENANT_ID':tenant_id_key,
                                #'OS_TENANT_NAME':'kycloudprod',
                                'OS_TENANT_NAME':tenant_name_key,
                                #'OS_USERNAME':'kycloudprod',
                                'OS_USERNAME':user_name_key,
                                #'OS_PASSWORD':'che001'
                                'OS_PASSWORD':password_key
                        }
                        keys = env_dist.keys()
                        for i in keys:
                                value = env_dist[i]
                                env_set.set_env(i,value)
                       #return os.environ.data
                        return env_dist

