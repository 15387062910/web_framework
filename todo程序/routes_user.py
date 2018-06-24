# __author__ = "wyb"
# date: 2018/6/21
from utils import log
from utils import random_str
from models import User
from routes_base import (
    session,
    current_user,
    http_response,
    redirect,
    template,
)


# 登录验证的装饰器 -> 验证当前用户是否登录
def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u is None:
            return redirect('/login')
        return route_function(request)

    return f


# # 主页路由
# @login_required
# def index(request):
#     """
#     主页的处理函数, 返回主页的响应
#     """
#     log("route_index")
#     body = template('index.html')
#     username = current_user(request)
#     body = body.replace('{{username}}', username)
#     return http_response(body)


# 登录路由
def login(request):
    """
    登录页面的路由函数
    """
    headers = {}
    result = ''
    # log('login, headers: ', request.headers)
    # log('login, cookies: ', request.cookies)
    cur_user = current_user(request)
    if cur_user is not None:
        username = cur_user.username
    else:
        username = "游客"

    if request.method == 'POST':
        form = request.form()
        u = User(form)
        # 登录验证成功
        if u.validate_login():
            # 查找用户
            user = User.find_by(username=u.username)

            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            # session[session_id] = u.username
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)

            # 下面是把用户名存入 cookie 中
            # headers['Set-Cookie'] = 'user={}'.format(u.username)

            # 登录成功后重定向到主页
            return redirect('/', headers=headers)

        # 登录验证失败
        else:
            result = '用户名或者密码错误'

    # 返回登录页面
    log("返回登录页面")
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    return http_response(body, headers=headers)


# 注册路由
def register(request):
    """
    注册页面的路由函数
    """
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            # result = '注册成功<br> <pre>{}</pre>'.format(User.all())
            return redirect('/login')
        else:
            result = '用户名或者密码长度至少6位'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    return http_response(body)


# 后台管理页面路由(GET)
def admin_users(request):
    """
    只有管理员才能访问这个页面, 其他用户访问会定向到 /login
    这个页面显示了所有的用户 包括 id username password
    :param request:
    :return: 是管理员就返回页面 不是就重定向到登录页面
    """
    u = current_user(request)
    if u is None:
        return redirect("/login")

    if u.is_admin():
        users = User.all()
        log("debug admin_users users: ", users)
        body = template("admin_users.html")
        body = body.replace("{{ user_info }}", str(users))
        return http_response(body)
    else:
        return redirect('/login')


# 后台管理页面路由(POST)
def admin_user_update(request):
    """
    /admin/users 页面中有一个表单  表单包括 id  password 两个 input
    管理员可以在这个表单中输入 id 和 新密码 来修改相应用户的密码
    这个表单发送 POST 请求到此路由下
    :param request:
    :return:
    """
    # 获得用户 id 和 新密码
    form = request.form()
    user_id = int(form.get('id', -1))
    new_password = form.get('password', '')

    u = User.find_by(id=user_id)
    if u is not None:
        u.password = new_password
        u.save()
    return redirect('/admin/users')


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # '/': index,
    '/login': login,
    '/register': register,
    '/admin/users': admin_users,
    '/admin/user/update': admin_user_update,
}
