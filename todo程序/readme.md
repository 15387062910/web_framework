## todo程序项目
### 程序说明
    实现登录注册功能(密码未加密) 
    实现todo: 发布一条信息 修改一条信息 删除一条信息 显示所有信息
    实现admin: 具有管理员权限的用户可以查看所有用户的账户名及密码
    未使用数据库，数据存储在data下的TXT文件中

### 目录结构
    data            以静态文本存储数据
    static          静态文件(图片 CSS JS)
    templates       模板文件(HTML)
    models.py       数据处理逻辑实现及相关类定义
    routes_base.py  路由函数中的基本功能
    routes_user.py  与用户功能相关的基本路由
    routes_todo.py  todo路由
    server.py       服务器主程序
    utils.py        封装小功能


### 运行
    直接运行目录下的server.py 然后在浏览器中输入localhost:3000/即可访问
    

### 详细说明
    见目录下的功能说明.py
   
   
 