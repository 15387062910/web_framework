# __author__ = "wyb"
# date: 2018/5/15
import socket

# 生成socket实例对象
sk = socket.socket()
# 绑定IP和端口
sk.bind(("127.0.0.1", 8888))
# 监听
sk.listen()

# 写一个死循环,一直等待客户端来连我
while 1:
    # 获取与客户端的连接
    conn, _ = sk.accept()
    # 接收客户端发来消息
    data = conn.recv(8096)
    print(data)
    # 给客户端回复消息 -》 完善的响应 -》 响应首行 响应体 响应内容
    conn.send(b'http/1.1 200 OK\r\ncontent-type:text/html; charset=utf-8\r\n\r\n')
    # 想让浏览器在页面上显示出来的内容都是响应正文
    conn.send(b'<h1>hello!</h1>')
    # 关闭
    conn.close()
    sk.close()
