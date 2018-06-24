# __author__ = "wyb"
# date: 2018/6/21
import json
import time
from utils import log


# 向文件中导入数据
def save(data, path):
    """
    向文件中保存数据
    :param data:   data 是 dict 或者 list
    :param path:   path 是保存文件的路径
    :return:
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save: ', path, s, data)
        f.write(s)


# 从文件中导出数据
def load(path):
    """
    从文件中导出数据
    :param path: 文件路径
    :return: 返回文件内容(列表形式)
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('the type of load: ', type(s))                                # str
        # log('the type of json.loads(s): ', type(json.loads(s)))           # list
        return json.loads(s)


class Model(object):
    """
    Model 是所有 model 的基类
    @... 是一个套路用法    @后面跟装饰器名  加在函数上面  用来给函数添加功能
    本类下面的@后面是 类方法的装饰器
    类方法:    类方法只能访问类变量，不能访问实例变量  cls表示类变量  谁调用的类名就是谁的 当然类方法也可以由对象来调用
    静态方法:  跟类没多大关系的函数，但是又想把这个方法的定义放入类中，就使用静态方法，静态方法所有对象均可以调用 也可以用类之间调用
    例如
    user = User()
    user.db_path() 返回 User.txt
    """

    @classmethod                                    # 加上这个表示是类方法
    def db_path(cls):                               # 获取类中数据对应的存储地址
        """
        cls 是类名, 谁调用的类名就是谁的
        cls 是 class 的缩写  是类变量
        """
        class_name = cls.__name__
        path = 'data/{}.txt'.format(class_name)
        return path

    @classmethod
    def all(cls):                                   # 获取类对应的所有对象
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls.new(m) 可以初始化一个 cls 的实例
        # 不明白就 log 看看这些都是啥
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):                     # find_by -> 根据传入的key和value 查找出第一个符合条件的对象
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all_object = cls.all()
        for m in all_object:
            # getattr(m, k) 等价于 m.__dict__[k]
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):                    # find_all -> 根据传入的key和value 查找出所有符合条件的对象
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all_object = cls.all()
        data = []
        for m in all_object:
            # getattr(m, k) 等价于 m.__dict__[k]
            if v == m.__dict__[k]:
                data.append(m)
        return data

    @classmethod
    def find(cls, uid):
        return cls.find_by(id=uid)

    @classmethod
    def delete(cls, uid):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == uid:
                index = i
                break
        # 判断是否找到了这个 id 的数据
        if index == -1:
            # 没找到
            pass
        else:
            models.pop(index)
            item = [m.__dict__ for m in models]
            path = cls.db_path()
            save(item, path)

    # # 删除 -> 有两种删除: (1)直接删除 这里使用直接删除     (2)间接删除(逻辑删除) 在数据中有一项 把该项置为特定的值表示删除
    # def remove(self):
    #     models = self.all()
    #     if self.__dict__.get('id') is not None:
    #         # 有 id 说明已经是存在于数据文件中的数据
    #         # 那么就找到这条数据并删除之
    #         index = -1
    #         for i, m in enumerate(models):
    #             if m.id == self.id:
    #                 index = i
    #                 break
    #         # 看看是否找到下标
    #         # 如果找到，就删除掉这条数据
    #         if index > -1:
    #             del models[index]
    #     # 保存
    #     res = [m.__dict__ for m in models]
    #     path = self.db_path()
    #     save(res, path)

    # 打印输出对象的__dict__中的所有项      __dict__ -> 存储对象中所有属性
    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        class_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(class_name, s)

    # 保存
    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        log('debug save')
        models = self.all()                 # 实例对象也可以调用类方法
        log('models', models)
        first_index = 0
        if self.__dict__.get('id') is None:
            # 加上 id
            if len(models) > 0:
                # log('用 log 可以查看代码执行的走向')
                # 不是第一个数据
                self.id = models[-1].id + 1
            else:
                # 是第一个数据
                log('first index', first_index)
                self.id = first_index
            models.append(self)
        else:
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换之
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            # 看看是否找到下标
            # 如果找到，就替换掉这条数据
            if index > -1:
                models[index] = self
        # 保存
        res = [m.__dict__ for m in models]
        path = self.db_path()
        save(res, path)


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        # 指定用户权限 普通权限是10 管理员权限是1
        self.role = int(form.get('role', 10))

    # 验证用户登录
    def validate_login(self):
        # 一种验证方法
        us = User.all()
        for u in us:
            if u.username == self.username and u.password == self.password:
                return True
        return False
        # 另一种验证方法
        # return self.username == 'gua' and self.password == '123'
        # u = User.find_by(username=self.username)
        # return u is not None and u.password == self.password

        # 这样的代码是不好的，不应该用隐式转换
        # return u and u.password == self.password
        # 0 None ''

    # 验证注册
    def validate_register(self):
        return len(self.username) > 5 and len(self.password) > 5

    # 判断用户是否是admin
    def is_admin(self):
        return self.role == 1


class Message(Model):
    """
    Message 是用来保存留言的 model
    """

    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')


class Todo(Model):
    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个todo 并且返回它
        Todo.new({'title': '吃饭'})
        :param form: 一个字典 包含了 todo 的数据
        :return: 创建的 todo 实例
        """
        # 下面一行相当于 t = Todo(form)
        t = cls(form, user_id)
        t.save()
        return t

    @classmethod
    def update(cls, todo_id, form):
        t = cls.find(todo_id)
        valid_names = [
            'title',
            'completed'
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                setattr(t, key, form[key])
        # 修改更新时间
        t.update_time = int(time.time())
        log("debug update_time: ", t)
        t.save()

    @classmethod
    def complete(cls, todo_id, completed):
        """
        用法很方便
        Todo.complete(1, True)
        Todo.complete(2, False)
        """
        t = cls.find(todo_id)
        t.completed = completed
        t.save()
        return t

    def is_owner(self, user_id):
        return self.user_id == user_id

    # 格式化创建时间和修改时间
    def ct(self):
        formats = '%Y/%m/%d %H:%M:%S'
        value = time.localtime(self.create_time)
        dt = time.strftime(formats, value)
        return dt

    def ut(self):
        formats = '%Y/%m/%d %H:%M:%S'
        value = time.localtime(self.update_time)
        dt = time.strftime(formats, value)
        return dt

    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.completed = False
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        # 添加创建和修改时间
        self.create_time = form.get('create_time', None)
        self.update_time = form.get('update_time', None)
        log("debug time: ", self.create_time, self.update_time)
        if self.create_time is None:
            self.create_time = int(time.time())
            self.update_time = self.create_time


def test():
    # users = User.all()
    # u = User.find_by(username='gua')
    # log('users', u)
    form = dict(
        username='gua',
        password='gua',
    )
    u = User(form)
    u.save()
    # u.save()
    # u.save()
    # u.save()
    # u.save()
    # u.save()
    # u = User.find_by(id=1)
    # u.username = '瓜'
    # u.save()


if __name__ == '__main__':
    test()
