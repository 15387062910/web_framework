# __author__ = "wyb"
# date: 2018/5/17
import time
import re
from wsgiref.simple_server import make_server


# 将返回不同的内容部分封装成函数
def index():
    with open("template/index.html", "rb") as f:
        res = f.read()
    pattern = "<p></p>"
    res2 = re.sub(pattern, str(time.strftime("%Y-%m-%d %H:%M:%S")), str(res, encoding="utf-8"))      # 替换内容
    return bytes(res2, encoding="utf-8")


def about():
    with open("template/about.html", "r", encoding="utf8") as f:
        s = f.read()
    return bytes(s, encoding="utf8")


# 定义一个专门用来处理404的函数
def f404():
    with open("template/404.html", "rb") as f:
        res = f.read()
    return res


# 定义一个url和实际要执行的函数的对应关系
list1 = [
    ("/index", index),
    ("/about", about),
]


def run_server(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8'), ])  # 设置HTTP响应的状态码和头信息
    url = environ['PATH_INFO']  # 取到用户输入的url
    func = None
    for i in list1:
        if i[0] == url:
            func = i[1]
            break
    if func:
        response = func()
    else:
        response = f404()
    return [response, ]


if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 8001, run_server)      # 启服务(监听端口然后执行run_server函数)
    httpd.serve_forever()                                   # 让服务一直启动

