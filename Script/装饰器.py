def login():
#    name = 'rain'
    name = 'alex'
    if name == 'alex':
        return True
    else:
        return False

def auth(func):
    def inner(*args,**kwargs):
        is_login = login()
        if not is_login:
            return '非法用户'
        temp = func(*args,**kwargs)
        print 'after'
        return temp
    return inner

@auth
def fetch_server_list(args):
    server_list = ['c1','c2','c3']
    return server_list

if __name__ == '__main__':
    print '-------------------'
    ret_list = fetch_server_list('test')
    print ret_list
