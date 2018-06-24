## web框架基础功能实现
### 说明
    此文件夹下代码均是使用python的socket模块、jinja2模块、wsgiref模块完成，模拟了web网站的一些功能
    一个py文件模拟一个web服务器
    template文件夹下是模板文件(HTML)

### 实现功能
    实现web服务端(): 见不完善的web服务端.py和完善的web服务端.py
    实现根据不同的url路径返回不同内容: 见根据不同路径返回不同内容xxx.py
    实现返回静态页面和动态页面:
        静态页面：写死的HTML文件
        动态页面：带参数的HTML文件，参数由后台替换
        见返回静态页面xxx.py 和 返回动态页面xxx.py
    用jinja2模板渲染库实现以上功能：见jinja2版xxx.py
    用wsgiref代替socket模块实现web服务器：见wsgiref版web服务器.py