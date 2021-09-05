from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import os
'''参考 启动并行任务 https://docs.python.org/zh-cn/3/library/concurrent.futures.html'''

DEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "download")
BASE_URL = "http://flupy.org/data/flags"
CC_LIST = ("CN", "US", "JP", "EG")

if not os.path.exists(DEST_DIR):
    os.mkdir(DEST_DIR)


def get_img(cc):
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    response = requests.get(url)
    return response.content

def save_img(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as f:
        f.write(img)

def download_one(cc):
    img = get_img(cc)
    save_img(img, cc.lower() + ".gif")
    return cc

# exector.map() 处理方法 ,注意：map 只能处理同一个调用处理对象
def download_many_01(cc_list):
    works = len(cc_list)
    with ThreadPoolExecutor(works) as exector: # 使用with来管理ThreadPoolExecutor
  # map方法和内置的map方法类似，不过exector的map方法会并发调用，返回一个由返回的值构成的生成器
        response = exector.map(download_one, cc_list)
    return len(list(response))

# exector.submit()和futures.as_completed()这个组合比exector.map()更灵活，submit()可以处理不同的调用函数和参数，而map只能处理同一个可调用对象。
def download_many_02(cc_list):
    with ThreadPoolExecutor(max_workers=5) as exector:
        future_list = []
        for cc in cc_list:
            # 使用submit提交执行的函数到线程池中，并返回futer对象（非阻塞）
            future = exector.submit(download_one, cc)
            future_list.append(future)
            print(cc, future)
        result = []
        # as_completed方法传入一个Future迭代器，然后在Future对象运行结束之后yield Future
        for future in as_completed(future_list):
            res = future.result()
            print(res, future)
            result.append(res)
    return len(result)




if __name__ == "__main__":
    #download_many_01(CC_LIST)
    download_many_02(CC_LIST)