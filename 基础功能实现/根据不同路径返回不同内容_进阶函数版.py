# __author__ = "wyb"
# date: 2018/5/16
# 将路由对应关系写在列表中，每次查路由对应的函数到这个列表中去查
# 就不用写if判断了,直接用url名字去找对应的函数名
import socket

# 生成socket实例对象
sk = socket.socket()
# 绑定IP和端口
sk.bind(("127.0.0.1", 8001))
# 监听
sk.listen()


# 定义一个处理/index的函数
def index(cur_url):
    ret = 'hello welcome to the {}'.format(cur_url)
    return bytes(ret, encoding="utf-8")


# 定义一个处理/about的函数
def about(cur_url):
    ret = 'hello welcome to the {}'.format(cur_url)
    return bytes(ret, encoding="utf-8")


# 定义一个专门用来处理404的函数
def f404(cur_url):
    ret = "你访问的这个{} 找不到".format(cur_url)
    return bytes(ret, encoding="utf-8")


url_func = [
    ("/index", index),
    ("/about", about),
]


# 写一个死循环,一直等待客户端来连我
while 1:
    # 获取与客户端的连接
    conn, _ = sk.accept()
    # 接收客户端发来消息
    data = conn.recv(8096)
    # 把收到的数据转成字符串类型
    data_str = str(data, encoding="utf-8")
    # print(data_str)
    # 用\r\n去切割上面的字符串
    l1 = data_str.split("\r\n")
    # print(l1[0])
    # 按照空格切割上面的字符串
    l2 = l1[0].split()
    url = l2[1]
    # 给客户端回复消息
    conn.send(b'http/1.1 200 OK\r\ncontent-type:text/html; charset=utf-8\r\n\r\n')
    # 想让浏览器在页面上显示出来的内容都是响应正文

    # 根据不同的url返回不同的内容
    # 去url_func里面找对应关系
    for i in url_func:
        if i[0] == url:
            func = i[1]
            break
    # 找不到对应关系就默认执行f404函数
    else:
        func = f404
    # 拿到函数的执行结果
    response = func(url)
    # 将函数返回的结果发送给浏览器
    conn.send(response)
    # 关闭连接而不关闭服务器
    conn.close()
