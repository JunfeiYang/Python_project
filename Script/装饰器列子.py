#!/usr/bin/env python
# --*-- coding:utf-8 -*-
# author: Andre Yang
def login(name):
    #name = 'andre'
    if name == 'andre':
        return "登陆成功"
    else:
        return "无效的用户名或密码"

def auth(func):  #func=fetch_server_list()
    def inner(args):
        temp = func(args)
        print temp
        is_login = login(temp)
        if not is_login:
            print is_login
            return "inviad user"
        else:
            print is_login
        print('处理完毕....')
        return temp
    return inner

@auth
def fetch_server_list(args):
    return args

if __name__ == '__main__':
    print('=============start==============')
    print('...start....')
    print('-----------jack------------')
    ret_list_jack = fetch_server_list('jack')
    print('-----------andre---------')
    ret_list_andre = fetch_server_list('andre')
    print('===============end================')