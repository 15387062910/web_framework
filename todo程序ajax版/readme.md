## todo程序项目 - ajax版本
### 程序说明
    实现todo: 输入todo内容发布todo 显示所有todo的内容和创建时间 可添加todo、编辑todo、删除todo、完成todo
    
### 功能说明
    添加todo: 在输入框中输入todo内容，然后点击后面的添加即可在下方添加一个todo
    编辑todo: 点击每一条todo中的编辑即可编辑当前todo，点击更新后编辑的内容将会更新到todo中
    删除todo: 点击每一条todo中的删除即可删除当前todo
    完成todo: 点击每一条todo中的完成即可完成当前todo 会标注出完成的todo

### 目录结构
    data                以静态文本存储数据
    templates           模板文件(HTML)
    static              静态文件(图片 CSS JS)
        base.js             基础js代码(封装一些常用功能: AJAX以及todo程序的前端API等)
        todo.js             与todo页面相关的js代码  
    models              数据处理逻辑实现及相关类定义
        __init__.py         基本model类定义    
        todo.py             todo类定义
    routes              路由处理
        routes_static.py    静态文件处理路由
        todo.py             todo基本路由
        api_todo.py         todo程序提供给前端的API
    server.py           服务器主程序
    utils.py            封装小功能
    log.txt             日志文件


### 运行
    直接运行目录下的server.py 然后在浏览器中输入localhost:3000/即可访问
    
