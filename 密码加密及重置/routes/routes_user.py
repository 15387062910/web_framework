# __author__ = "wyb"
# date: 2018/6/25
from models import User
from utils import log
from utils import random_str
from .routes_base import template
from .routes_base import response_with_headers
from .routes_base import redirect


# 首页
def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'

    msg = request.query.get("msg", "")
    if msg == "1":
        msg = "登录成功"
    body = template('index.html')
    body = body.replace("{{ msg }}", msg)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 登录
def login(request):
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    log('login, cookies', request.cookies)

    result = ""
    body = template('login.html')

    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            # 登录后重定向到首页
            return redirect('/?msg=1')
        else:
            result = "登录名或密码错误"

    body = body.replace("{{ result }}", result)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 注册
def register(request):
    """
    注册页面的路由函数
    """
    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register() is not None:
            # 注册成功后 定向到登录页面
            log('注册成功: ', u)
            return redirect('/login')
        else:
            # 注册失败 定向到注册页面
            return redirect('/register')
    # 显示注册页面
    body = template('register.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 重置密码
def reset(request):
    """
    重置密码后台路由: 显示页面 提交重置
    :param request:
    :return:
    """
    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    body = template("reset.html")

    # get请求 返回页面
    if request.method == "GET":
        body = body.replace("{{ result }}", "输入以上信息重置密码")
    # post请求 处理重置
    else:
        # 两次输入的旧密码一样就验证 否则不验证
        form = request.form()
        name = form.get("username", "")
        u = User.find_by(username=name)
        if u is not None:
            log("before change pwd: ", u)
            res = u.change_pwd(form)
            log("after change pwd: ", res["data"])
            body = body.replace("{{ result }}", res["msg"])
        else:
            body = body.replace("{{ result }}", "输入的用户名不存在!")

    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 路由字典
route_dict = {
    '/': index,
    '/login': login,
    '/register': register,
    '/reset': reset,
}
