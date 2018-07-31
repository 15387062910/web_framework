// 这是基础js文件 放一些通用性的js代码

// 封装输出
var log = function() {
    // 使用方法: log(666, "333")
    // 该函数可以给任何多个参数 将输出到控制台
    console.log.apply(console, arguments)
};

// 封装元素选择器
var e = function(sel) {
    // sel -> CSS选择器语法: #id .class
    return document.querySelector(sel)
};

// 将timestamp(时间戳)格式转化成合适的时间格式
var timeString = function (timestamp) {
    t = new Date(timestamp * 1000);
    t = t.toLocaleDateString() + " " + t.toLocaleTimeString();

    return t;
};
// 测试如下:
// log(timeString(1532958089));
// 2018/7/30 下午9:41:29


/*
 ajax 函数
*/
var ajax = function(method, path, data, reseponseCallback) {
    var r = new XMLHttpRequest();
    // 设置请求方法和请求地址
    r.open(method, path, true);
    // 设置发送的数据的格式为 application/json
    r.setRequestHeader('Content-Type', 'application/json');
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            // log("r.response: ", typeof r.response); // string
            reseponseCallback(r.response);
        }
    };
    // 把数据转换为 json 格式字符串 -> 字典转换成字符串
    data = JSON.stringify(data);
    // 发送请求
    r.send(data);
};


// TODO的前端API:
// 获取所有todo
var apiTodoAll = function(callback) {
    // callback -> 回调函数 将在接收到后端的响应后调用
    var path = '/api/todo/all';
    ajax('GET', path, '', callback);
};


// 增加一个todo
var apiTodoAdd = function(form, callback) {
    // callback -> 回调函数 将在接收到后端的响应后调用
    var path = '/api/todo/add';
    ajax('POST', path, form, callback);
};
// 测试如下:
// 注意 此时回调函数中没有写与操作前端页面相关的代码 所以要看到操作结果就要刷新页面 下面的测试同理
// apiTodoAdd({"title": "wyb666"}, function (response) {
//     log("todo的add测试成功!");
//     log("服务器返回的响应: ", response);
//     log("请刷新页面查看效果!");
// });


// 删除一个todo
var apiTodoDelete = function (id, callback) {
    // callback -> 回调函数 将在接收到后端的响应后调用
    var path = '/api/todo/delete?id=' + id;
    ajax('GET', path, '', callback);
};
// 测试如下:
// apiTodoDelete('1', function (response) {
//     log("todo的delete测试成功!");
//     log("服务器返回的响应: ", response);
//     log("请刷新页面查看效果!");
// });


// 更新一个todo
var apiTodoUpdate = function (data, callback) {
    // callback -> 回调函数 将在接收到后端的响应后调用
    var path = '/api/todo/update';
    ajax('POST', path, data, callback);
};
// // 测试如下:
// apiTodoUpdate({
//     "id": "1",
//     "title": "被修改后的内容"
// }, function (response) {
//     log("todo的update测试成功!");
//     log("服务器返回的响应: ", response);
//     log("请刷新页面查看效果!");
// });


// 完成一个todo
var apiTodoComplete = function (data, callback) {
    // callback -> 回调函数 将在接收到后端的响应后调用
    var path = '/api/todo/complete';
    ajax('POST', path, data, callback);
};

