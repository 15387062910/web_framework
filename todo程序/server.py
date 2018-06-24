# __author__ = "wyb"
# date: 2018/6/21
import socket
import urllib.parse
from utils import log
from routes_base import route_static
from routes_user import route_dict
from routes_base import error
# 注意要用 from import as 来避免重名
from routes_todo import route_dict as todo_route


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        # 清空 headers
        self.headers = {}
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除 cookies
        self.cookies = {}
        self.add_cookies()

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


# 获取Request对象
request = Request()


# 解析path
def parsed_path(path):
    """
    path: /?message=hello&author=wyb
    ->
    path: /
    query:
    {
        'message': 'hello',
        'author': 'wyb',
    }
    :param path: 路径
    :return:    返回 真正的路径 和 后面的参数
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


# 根据路由调用对应的路由函数返回响应结果
def response_for_path(path):
    """

    :param path: 路由
    :return: 响应结果
    """

    # 从path 分解出 真正的path 和 后面的参数
    path, query = parsed_path(path)

    # 设置 request 中的 path 和 query
    request.path = path
    request.query = query
    log('path and query', path, query)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    # 基本路由字典
    r = {
        '/static': route_static,
        # 以下路由及其他路由将在后面动态添加进来
        # '/': route_index,
        # '/login': route_login,
        # '/messages': route_message,
    }
    # 动态添加路由字典
    r.update(route_dict)
    r.update(todo_route)
    response = r.get(path, error)

    return response(request)


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    if host == '':
        host_name = "localhost"
    else:
        host_name = host
    log('start at', '{}:{}'.format(host_name, port))
    with socket.socket() as s:
        # 绑定host和端口
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串   监听请求并接受请求
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, r))
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue

            # 分解请求信息:
            path = r.split()[1]                                                 # 获取请求路径 eg: /
            request.method = r.split()[0]                                       # 设置 request 的 method
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])    # 设置 request 的 请求首行
            request.body = r.split('\r\n\r\n', 1)[1]                            # 把 body 放入 request 中

            # 处理请求:
            response = response_for_path(path)                      # 用 response_for_path 函数来得到 path 对应的响应内容
            log('debug ******', 'sendall')
            connection.sendall(response)                            # 把响应发送给客户端
            log('debug ****', 'close')

            # 处理完请求, 关闭连接
            connection.close()
            log('debug **', 'closed')


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='127.0.0.1',
        port=3000,
    )
    # 如果不了解 **kwargs 的用法, 上过基础课的请复习函数, 新同学自行搜索
    run(**config)
