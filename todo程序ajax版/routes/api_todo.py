import json
from routes.session import session
from utils import (
    log,
    redirect,
    http_response,
    json_response,
)
from models.todo import Todo

# TODO的后端API:
# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据


def all(request):
    """
    返回所有的todo
    :param request:
    :return: json格式数据
    """
    todo_list = Todo.all()
    # 把todo对象转化成字典
    todos = [t.json() for t in todo_list]
    return json_response(todos)


def add(request):
    """
    接受浏览器发过来的添加 todo请求
    添加数据并返回给浏览器
    :param request:
    :return: json格式数据
    """
    # 得到浏览器发送的json格式数据
    # 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用Request对象中新增加的json函数 来获取 格式化后的 json 数据(字典)
    form = request.json()
    # 创建一个 todo项
    t = Todo.new(form)
    # 把创建好的 todo返回给 浏览器
    # 下面的json方法是todo对象的json方法 是把对象变成字典
    # 然后json_response将字典转化成字符串
    return json_response(t.json())


def delete(request):
    """
    通过下面这样的链接来删除一个todo
    /delete?id=1
    :param request:
    :return:
    """
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    # 下面的json方法是todo对象的json方法 是把对象变成字典
    # 然后json_response将字典转化成字符串
    return json_response(t.json())


def update(request):
    """
    更新todo
    :param request:
    :return:
    """
    # 得到浏览器发送的json格式数据
    # 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用Request对象中新增加的json函数 来获取 格式化后的 json 数据(字典)
    form = request.json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.json())


def complete(request):
    """
    完成todo
    :param request:
    :return:
    """
    # 得到浏览器发送的json格式数据
    # 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用Request对象中新增加的json函数 来获取 格式化后的 json 数据(字典)
    form = request.json()
    todo_id = int(form.get('id'))
    completed = form.get('complete')
    if completed == "0":
        t = Todo.complete(todo_id, False)
    else:
        t = Todo.complete(todo_id)
    return json_response(t.json())


route_dict = {
    '/api/todo/all': all,
    '/api/todo/add': add,
    '/api/todo/delete': delete,
    '/api/todo/update': update,
    '/api/todo/complete': complete,
}
