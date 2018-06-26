# __author__ = "wyb"
# date: 2018/6/25
import time
import random


# 向屏幕输出日志
def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    formats = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(formats, value)
    print(dt, *args, **kwargs)


# 生成随机字符串
def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


