# __author__ = "wyb"
# date: 2018/5/15
import socket

# 生成socket实例对象
sk = socket.socket()
# 绑定IP和端口
sk.bind(("127.0.0.1", 8001))
# 监听
sk.listen()

# 写一个死循环,一直等待客户端来连我
while 1:
    # 获取与客户端的连接
    conn, _ = sk.accept()
    # 接收客户端发来消息
    data = conn.recv(8096)
    # 把收到的数据转成字符串类型
    data_str = str(data, encoding="utf-8")
    # print(data_str)

    l1 = data_str.split("\r\n")     # 用\r\n去切割上面的字符串
    l2 = l1[0].split()              # 按照空格切割上面的字符串
    url = l2[1]                     # 取得url
    # 给客户端回复消息
    conn.send(b'http/1.1 200 OK\r\ncontent-type:text/html; charset=utf-8\r\n\r\n')

    # 根据不同的url返回不同的内容
    if url == "/index":
        response = b'<h1>hello welcome to index!</h1>'
        print(response)
    elif url == "/about":
        response = b'<h1>write by wyb</h1>'
        print(response)
    else:
        response = b'<h1>404! not found!</h1>'
        print(response)
        conn.send(response)
        break
    conn.send(response)

# 关闭连接但是不关闭服务器
conn.close()
