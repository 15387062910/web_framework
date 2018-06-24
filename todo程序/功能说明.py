# __author__ = "wyb"
# date: 2018/6/21
# 程序结构说明
"""
一个简单的todo 程序项目, 包含的文件如下:
data            以静态文本存储数据
static          静态文件(图片 CSS JS)
templates       模板文件(HTML)
models.py       数据处理及相关类定义(Model User Message Todo)
routes_base.py  路由函数中的基本功能(比如返回模板文件、重定向、返回静态文件、获得当前用户对象等功能)
routes_user.py  基本路由(与用户功能相关的路由: 登录 注册 admin 以及实现登录验证)
routes_todo.py  todo路由(显示todo、增加todo、删除todo、更新todo)
server.py       服务器主程序
utils.py        封装与程序逻辑无太大关系的小功能(log等) -> 可以直接复用到其他项目中

和todo功能相关的:
    routes_todo.py 包含了项目的所有路由函数 实现以下功能:
        显示所有todo
        增加todo
        更新todo
        删除todo
    todo.py
        包含了 Todo Model, 用于处理数据
    templates/todo_index.html
        显示所有 todo 的页面
    templates/todo_edit.html
        显示编辑 todo 的界面


把 todo 改写为带用户功能的高级版
    涉及到不同数据的关联
    关联数据在服务器/浏览器之间的传递


# 统一定义一个函数统一检测用户是否登录:
def login_required(route_function):
    def func(request):
        user_name = current_user(request)
        log("登录鉴定: ", username)
        u = User.find_by(username=user_name)
        if u is None:
        # 没登录 就不让你看 重定向到login
            return redirect('/login')
        return route_function(request)
    return func

# 统一定义一个函数统一检测用户是否登录也可以这样写:
def login_required(route_function):
    def func(request):
        user_name = current_user(request)
        log("登录鉴定: ", username)
        if username == "游客":
        # 没登录 就不让你看 重定向到login
            return redirect('/login')
        return route_function(request)
    return func

"""


"""
程序执行思路(server.py + routes_user.py):
    建立host和端口
    监听请求
    接受请求
        分解请求信息
            method  -> 请求方法
            path    -> 请求真实path     
            query   -> 请求参数 
            body    -> 请求体内容
        保存请求
            临时保存，用完就丢
    处理请求
        获取路由字典
            path和响应函数的映射字典
        根据请求的path和字典处理请求并获得返回页面
            routes.py中涉及的路由:
                主页
                    返回页面
                登录
                    处理post请求
                        对比post数据和用户数据
                        返回登录结果
                    返回页面
                注册
                    处理post请求
                        对比post数据和注册规则
                        保存合法的注册信息
                            保存到User.txt
                        返回注册结果
                    返回页面
                留言板
                    处理post请求
                        将post的数据加入留言列表(临时数据 运行一次存在一次)
                    返回页面
                        包含留言列表
                静态资源（图片）
                    根据query的内容返回对应的资源
        返回响应内容
    发送响应内容
    关闭请求连接


MVC  设计模式(一个非常有名经典的套路)
Modal       数据
view        显示
controller  控制器
"""


# todo add的流程解析:
"""
点击添加按钮增加一个新的 todo 的时候, 程序的流程如下(包含原始 HTTP 报文):
1、浏览器提交一个表单给服务器(发送 POST 请求)
    POST /todo/add HTTP/1.1
    Content-Type: application/x-www-form-urlencoded

    title=xxx

2、服务器解析出表单的数据, 并且增加一条新数据, 并返回 302 响应
    HTTP/1.1 302 REDIRECT                   # 这里REDIRECT不是必须的 你爱写啥就写啥
    Location: /todo

3、浏览器根据 302 中的地址, 自动发送了一条新的 GET 请求
    GET /todo HTTP/1.1
    Host: ....

4、服务器给浏览器一个页面响应
    HTTP/1.1 200 OK
    Content-Type: text/html
    Content-Length: ...

    <html>
        ....
    </html>

5、浏览器把新的页面显示出来

"""


# 下面是一些 HTTP 请求和响应的例子:
# POST请求
"""
POST /login?id=2 HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Content-Length: 25
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Cookie: Pycharm-7367d7d5=bf094603-b9e9-4994-9ebd-564f1f5ad2c0

username=wyb&password=666
"""


# 响应
"""
2018/06/22 19:42:48 login 的响应
HTTP/1.1 210 VERY OK
Content-Type: text/html
Set-Cookie: user=gua1

<html>
"""


# GET请求
"""
GET /login HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Cookie: user=wyb
"""
