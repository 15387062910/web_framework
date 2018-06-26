# __author__ = "wyb"
# date: 2018/6/25
import json
import hashlib
from utils import log


# 向文件中导入数据
def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


# 从文件中读出数据
def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


# Model 是一个 ORM（object relation mapper）
# 好处就是不需要关心存储数据的细节，直接使用即可
class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """
    @classmethod
    def db_path(cls):
        """
        cls 是类名, 谁调用的类名就是谁的
        classmethod 有一个参数是 class(这里我们用 cls 这个名字)
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls(m) 可以初始化一个 cls 的实例
        # 不明白就 log 大法看看这些都是啥
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否找到了这个 id 的数据
        if index == -1:
            # 没找到
            pass
        else:
            models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            return

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        # log('debug save')
        models = self.all()
        # log('models', models)
        # 如果没有 id，说明是新添加的元素
        if self.id is None:
            # 设置 self.id
            # 先看看是否是空 list
            if len(models) == 0:
                # 我们让第一个元素的 id 为 1（当然也可以为 0）
                self.id = 1
            else:
                m = models[-1]
                # log('m', m)
                self.id = m.id + 1
            models.append(self)
        else:
            # index = self.find(self.id)
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            log('debug', index)
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    # 加盐加密
    @staticmethod
    def salted_password(password, salt="`1234567890~!@#$%^&*()-=[];'\/,./ZXCVBNSADFYWQET"):
        # salt:  "`1234567890~!@#$%^&*()-=[];'\/,./ZXCVBNSADFYWQET"
        def md5hex(ascii_str):
            return hashlib.md5(ascii_str.encode('ascii')).hexdigest()

        # 普通加密
        hash1 = md5hex(password)
        # 加盐加密
        hash2 = md5hex(hash1 + salt)
        return hash2

    # 普通加密
    @staticmethod
    def hash_password(pwd):
        # 用 ascii 编码转换成 bytes 对象
        pwd = pwd.encode('ascii')
        # 创建 md5 对象
        m = hashlib.md5(pwd)
        return m.hexdigest()

    # 注册
    def validate_register(self):
        pwd = self.password
        self.password = self.salted_password(pwd)
        # 用户名已存在就不允许注册 否则可以注册
        if User.find_by(username=self.username) is None:
            self.save()
            return self
        else:
            return None

    # 登录
    def validate_login(self):
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.salted_password(self.password)
        else:
            return False

    # 修改密码
    def change_pwd(self, form):
        # 输入两次旧密码不一样
        pwd1 = form.get("pwd1", "")
        pwd2 = form.get("pwd2", "")
        if pwd1 != pwd2:
            res = {
                "msg": "两次输入的旧密码不一样",
                "data": None,
            }
            return res

        # 输入的旧密码正确就重置 否则就不重置
        new_pwd = form.get("new_pwd", "")
        if self.salted_password(pwd1) == self.password:
            self.password = self.salted_password(new_pwd)
            self.save()
            res = {
                "msg": "重置密码成功",
                "data": self,
            }
        else:
            res = {
                "msg": "输入的旧密码错误!",
                "data": None,
            }
        return res


