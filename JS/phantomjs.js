// console.log('Hello World!');
// // 创建页面对象
// var page = require('webpage').create();

// // 打开网页, 参数1为网址，参数2为回调函数。打开成功则返回success, 否则fail。只要接收到服务器返回的消息就success。
// page.open('http://www.5izan.site', function(status) {
//     console.log(status);
//     phantom.exit();
// });

// // 使用post方法打开网页
// var page = require('webpage').create();
// var postBody = 'user=username&password=password';
// page.open('http://www.baidu.com', 'POST', postBody, function(status){
//     console.log('Status: ' + status);
//     // phantom.exit();
// });

// 更多配置
var page = require('webpage').create();
var settings = {
    operation:'POST',
    encoding:'utf8',
    headers:{
        'Content-Type': 'application/json'
    },
    data: JSON.stringify({
        some: 'data',
        another: ['custom', 'data']
    })
};
page.open('http://www.baidu.com', settings, function(status){
    console.log(settings);
    console.log('Status: ' + status);
});