
// 生成todotodoApi的对象
var todoApi = new TodoApi();

var todoTemplate = function(todo) {
    var title = todo.title;
    var id = todo.id;
    var t = timeString(todo.ct);
    var complete = "";
    if(todo.completed === true){
        complete = "complete";
    }
    // data-xx 是自定义标签属性的语法
    // 通过这样的方式可以给任意标签添加任意属性
    // 这样的自定义属性可以通过 element.dataset.xx 来获取
    var t = `<div class="todo-cell ${complete}" id="todo-${id}" data-id="${id}"><button class="todo-complete">完成</button><button class="todo-edit">编辑</button><button class="todo-delete">删除</button><span class="todo-title">${title}</span>&nbsp;&nbsp;<time class="todo-ct">创建时间: ${t}</time><br></div>`;
    return t;
};

var insertTodo = function(todo) {
    var todoCell = todoTemplate(todo);
    // 插入todo-list
    var todoList = e('.todo-list');
    todoList.insertAdjacentHTML('beforeend', todoCell)
};

var insertEditForm = function (editButton, containerDiv) {
    log(editButton, containerDiv);
    // 如果以及有了输入框就直接返回 否则添加输入框
    for(var i=0; i<containerDiv.children.length; i++){
        var item = containerDiv.children[i];
        // log("item", item);
        if(item.classList.contains("todo-edit-form")){
            return
        }
    }
    containerDiv.insertAdjacentHTML('beforeend', "<div class='todo-edit-form'><input type='text' placeholder='请输入新内容' class='todo-edit-input'><button class='todo-update'>更新</button></div>");
};

var loadTodos = function() {
    // 调用 ajax todoApi 来载入数据
    todoApi.all(function(response) {
        // 收到返回的数据, 将所有的todo插入到页面中 字符串转化成数组
        var todos = JSON.parse(response);
        // 循环添加到页面中
        for(var i = 0; i < todos.length; i++) {
            var todo = todos[i];
            insertTodo(todo)
        }
    })
};

var bindEventTodoAdd = function() {
    var b = e('#id-button-add');
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-todo');
        var title = input.value;
        log('click add', title);
        var form = {
            title: title
        };
        todoApi.add(form, function(response) {
            // 收到返回的数据, 插入到页面中 字符串转化成字典
            var todo = JSON.parse(response);
            insertTodo(todo);
        })
    })
};

var bindEventTodoDelete = function () {
    // 实现机制: 事件委托
    var todoList = e('.todo-list');
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function(event){
        log(event, event.target);
        var self = event.target;
        if(self.classList.contains('todo-delete')){
            // 删除todo
            var todoCell = self.parentElement;
            var todoId = todoCell.dataset.id;
            todoApi.delete(todoId, function (r) {
                log('删除数据成功: ', todoId);
                log(r);
                todoCell.remove();
            })
        }

    })
};

var bindEventTodoEdit = function () {
    // 实现机制: 事件委托
    var todoList = e('.todo-list');
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function(event){
        // log(event, event.target);
        var self = event.target;
        log(self);
        if(self.classList.contains('todo-edit')){
            // 在todo这一项后面加一个输入框以及确认按钮
            insertEditForm(self, self.parentElement);
        }

    })
};

var bindEventTodoUpdate = function () {
    // 实现机制: 事件委托
    var todoList = e('.todo-list');
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function(event){
        // log(event, event.target);
        var self = event.target;
        if(self.classList.contains('todo-update')){
            log("点击了todo-update");
            var editForm = self.parentElement;
            var input = editForm.querySelector('.todo-edit-input');
            var title = input.value;
            // 可以用closest方法 找到最近的直系父节点
            var todoCell = self.closest('.todo-cell');
            var todoId = todoCell.dataset.id;
            var form = {
                'id':todoId,
                'title': title
            };
            todoApi.update(form, function (response) {
                // log("服务器返回的响应: ", response);
                // 找到todo 然后替换todo中的内容
                log(typeof response);
                log(response);
                var todo = JSON.parse(response);
                var selector = '#todo-' + todo.id;
                var todoCell = e(selector);
                var titleSpan = todoCell.querySelector('.todo-title');
                titleSpan.innerHTML = todo.title;
                // 移去编辑框
                editForm.remove();
            });

        }

    })
};

var bindEventTodoComplete = function () {
    // 实现机制: 事件委托
    var todoList = e('.todo-list');
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function(event){
        log(event, event.target);
        var self = event.target;
        if(self.classList.contains('todo-complete')){
            log("点击了todo-complete");
            var todoCell = self.parentElement;
            var todoId = todoCell.dataset.id;
            var form = {
                'id':todoId
            };
            if(self.classList.contains('complete')){
                form["complete"] = "0"
            }
            todoApi.complete(form, function (response) {
                log("服务器返回的响应: ", response);
                var todo = JSON.parse(response);
                log(todo);
                if(todo.completed===true){
                    self.parentElement.classList.add('complete');
                }
            });

        }

    })
};

// 绑定所有事件
var bindEvents = function() {
    // 添加 删除 编辑 更新 完成
    bindEventTodoAdd();
    bindEventTodoDelete();
    bindEventTodoEdit();
    bindEventTodoUpdate();
    bindEventTodoComplete();
};

var __main = function() {
    bindEvents();
    loadTodos();
};

__main();
