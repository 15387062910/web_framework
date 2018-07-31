from routes.session import session
from utils import (
    log,
    redirect,
    template,
    http_response,
)


# 主页路由函数 -> '/'
def main_index(request):
    """
    将访问主页重定向到todo的首页
    :param request:
    :return:
    """
    return redirect('/todo_list/index')


# todo的主页路由函数 -> '/todo_list/index'
def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    body = template('todo_index.html')
    return http_response(body)


route_dict = {
    # 以下三个路径本质上都是返回todo首页 即返回todo_index.html
    '/': main_index,
    '/index': main_index,
    '/todo_list/index': index,
}
