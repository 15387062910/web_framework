# __author__ = "wyb"
# date: 2018/6/21
from utils import log
from models import Todo
from routes_base import (
    redirect,
    current_user,
    http_response,
    error,
    template,
)
from routes_user import login_required


# todo 首页路由
@login_required                 # 本质: login_required(index) 实现登录验证 验证用户是否登录 未登录重定向到登录页面
def index(request):
    """
    todo 首页的路由函数
    可以根据 不同的登录用户 显示不同登录用户的todo
    例如: wyb访问就只显示 wyb的todo   Alex访问就只显示 Alex的路由
    另外 如果未登录就访问该路由  将重定向到登录页面 -> 重定向通过装饰器实现
    """
    # headers = {
    #     'Content-Type': 'text/html',
    # }

    # 获得当前用户
    u = current_user(request)
    # 根据当前用户获得所有的todo
    todo_list = Todo.find_all(user_id=u.id)

    # 生成一个todo_s列表 列表中每一项是一个todo
    todo_s = []
    for t in todo_list:
        log("create_time and update_time debug: ", t.create_time, t.update_time)
        edit_link = '  <a href="/edit?id={}">编辑</a>'.format(t.id)
        delete_link = '  <a href="/delete?id={}">删除</a>'.format(t.id)
        s = '<h3>{} : {} {} {} {} {}</h3>'.format(
            t.id, t.title, "  create_time: " + t.ct(),
            "  update_time: " + t.ut(), edit_link, delete_link
        )
        todo_s.append(s)

    # 拼接字符串
    todo_html = ''.join(todo_s)

    # 替换模板文件中的标记字符串
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)

    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    # header = response_with_headers(headers)
    # r = header + '\r\n' + body
    # return r.encode(encoding='utf-8')
    return http_response(body)


# todo add路由
@login_required
def add(request):
    """
    用于增加新 todo 的路由函数
    """
    # 获得当前用户
    u = current_user(request)

    # 获取POST请求提交的数据并新建todo对象 然后保存
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.save()

    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/')


# todo edit路由
@login_required
def edit(request):
    """
    todo edit 的路由函数 返回 edit 页的响应
    /edit?id=1
    """
    # 获得当前用户
    u = current_user(request)

    # 得到当前编辑的todo 的 id 并根据其获得todo对象
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)

    # todo_id 不正常 说明该页面不存在 就返回404
    if todo_id < 1:
        return error(404)

    # 如果todo的用户id 不等于 当前用户id 或者 todo的id不存在 就重定向到首页 -> 实现权限控制
    if t is None or t.user_id != u.id:
        log("权限控制-edit")
        return redirect('/')

    # 替换模板文件中的标记字符串
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))

    return http_response(body)


# todo update路由
@login_required
def update(request):
    """
    用于增加新 todo 的路由函数
    edit页面的后台逻辑
    """
    # 获得当前用户
    u = current_user(request)

    # 根据提交的数据 进行修改并保存todo 只需更改title
    if request.method == 'POST':
        form = request.form()
        print('debug update: ', form)

        # 获取todo_id和todo对象
        # todo_id从query中获取
        todo_id = int(request.query.get('id', -1))
        # todo_id从form中获取
        # todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)

        # 如果todo的用户id 不等于 当前用户id 或者 todo的id不存在 就重定向到首页 -> 实现权限控制
        if t is None or t.user_id != u.id:
            log("权限控制-update")
            return redirect('/')

        # # 通过权限控制保存修改
        # t.title = form.get('title', t.title)
        # # 修改 update_time

        # 修改
        t.update(todo_id, form)

    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/')


# todo delete路由
@login_required
def delete(request):
    """
    通过下面这样的链接来删除一个 todo
    /delete?id=1
    :param request:
    :return: todo_id 不正常返回404 当前todo的用户id 不等于 当前登录用户的id 重定向到登录页面  删除完毕重定向到首页
    """
    # 获得当前用户
    u = current_user(request)

    # 得到当前 编辑的todo 的 id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)

    # todo_id 不正常 说明该页面不存在 就返回404
    if todo_id < 0:
        return error(404)

    # 如果todo的用户id 不等于 当前用户id 就重定向到 登录页面
    if t.user_id != u.id:
        return redirect('/login')

    # t不为空 就删除t
    if t is not None:
        t.delete(todo_id)

    return redirect('/')


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # GET 请求, 显示页面
    '/': index,
    '/edit': edit,
    # POST 请求, 处理数据
    '/add': add,
    '/delete': delete,
    '/update': update,
}
