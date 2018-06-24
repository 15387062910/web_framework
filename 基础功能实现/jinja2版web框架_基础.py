# __author__ = "wyb"
# date: 2018/5/17
from wsgiref.simple_server import make_server
from jinja2 import Template


def index():
    with open("template/jinja2_test.html", "r", encoding="utf-8") as f:
        data = f.read()
    template = Template(data)  # 生成模板文件
    ret = template.render({"name": "wyb", "hobby_list": ["写代码", "骑车"]})     # 把数据填充到模板中
    return [bytes(ret, encoding="utf-8"), ]


def about():
    with open("template/about.html", "rb") as f:
        data = f.read()
    return [data, ]


def home():
    with open("template/index.html", "rb") as f:
        data = f.read()
    return [data, ]


# 定义一个url和函数的对应关系
URL_LIST = [
    ("/index", index),
    ("/about", about),
    ("/home", home),
]


def run_server(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8'), ])  # 设置HTTP响应的状态码和头信息
    url = environ['PATH_INFO']      # 取到用户输入的url
    func = None                     # 将要执行的函数
    for i in URL_LIST:
        if i[0] == url:
            func = i[1]     # 去之前定义好的url列表里找url应该执行的函数
            break
    if func:                # 如果能找到要执行的函数
        return func()       # 返回函数的执行结果
    else:
        return [bytes("404没有该页面", encoding="utf8"), ]


if __name__ == '__main__':
    httpd = make_server('', 8001, run_server)       # 启动服务
    print("Serving HTTP on port 8001...")
    httpd.serve_forever()                           # 让服务一直运行
