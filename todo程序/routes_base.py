# __author__ = "wyb"
# date: 2018/6/21
# 封装路由函数中常用功能
from models import User
from utils import log

# session 可以在服务器端实现过期功能
session = {}


# 根据request中的数据以及session确认当前用户 返回用户对象 User
def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, -1))
    u = User.find_by(id=user_id)
    return u


# 读取模板文件
def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


# 把headers(响应头)封装到header(响应首行)中
def response_with_headers(headers, code=200):
    """
    Set-Cookie: user=wyb
    :param headers: 比如说 Content-Type: text/html -> 返回内容的类型
    :param code: 响应状态码 比如说 200 或者 302
    :return:
    """
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)  # 响应首行

    # 向响应首行中添加headers(响应头内容)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


# 把body和header(headers)一起封装成响应
def http_response(body, headers=None):
    """

    :param body: 响应体内容
    :param headers: 可选的响应头 key-value
    :return: 响应内容(响应首行 响应头 响应体)
    """
    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'                      # 响应首行
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)                                    # 添加headers(响应头内容)
                           for k, v in headers.items()])
    r = header + '\r\n' + body                                                          # 响应内容
    return r.encode(encoding='utf-8')


# 重定向
def redirect(url, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    注: 302 -> 临时重定向     301 -> 永久重定向
    :param url: 重定向url
    :param headers: 要添加进响应的headers
    :return:
    """
    log("redirect: ", url)
    h = {
        'Location': url,
    }
    # 如果传入headers 就将 headers并入h
    if headers is not None:
        h.update(headers)
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    r = response_with_headers(h, 302) + '\r\n'
    # log("redirect content: ", r)
    return r.encode('utf-8')


# 返回404
def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


# 静态文件路由
def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img

