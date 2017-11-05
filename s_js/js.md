# 基本知识
## 数据类型
* 数字型：包括整数和浮点数  
* 逻辑型：只有 true 或 false
* 字符串型
## 变量赋值  
`var varibleName = variableValue  `
## 数据操作
`% 求模`
## 数据操作符
`x+=y; # 即 x = x+y，必须先赋好值。`

## 常用操作
* 在当前文档中追加内容，可以是html标签
```
document.write('<p>document.write</p>')
```


## 常用事件

|事件属性|触发|
|:---|:---|
|onblur|元素失去焦点|
|onfocus|元素获得焦点|
|onchange|改变字段的内容|
|onclick|鼠标单击|
|ondblclick|鼠标双击|
|onerror|载入图像或文档时出错|
|onkeypress|按下键或保持按下|
|onkeyup|释放键|
|onload|页面或图像完成载入|
|onmousedown|按下一个鼠标按钮|
|onmousemove|移动鼠标|
|onmouseout|鼠标离开一个元素|
|onmouseover|鼠标进入一个元素|
|onmouseup|释放一个鼠标按钮|
|onresize|改变窗口大小|
|onselect|选择一些文本|
|onunload|页面退出|
|||


* 点击onclick()
```
<input type="button" id="mybutton" value="hi there"
    onclick("alert('onclick')"); />
```
* <body>的onload(), 在用户看到页面前就执行js代码
```
<head>
    <script>
        function welcome(){
            alert("warning");
        }
    </script>
</head>
```
.onload();

## 知识点
* document(文档)对象:浏览器把网页视为一个对象层次，包括页面中的所有元素及其属性。  
* 顶层对象是windo， document是window对象的子对象。
* document对象属性   

|属性|描述|
|:----|:----|
|cokkie|返回文档中所有Cookie的名字/值对|
|documentMode|返回浏览器用于显示文档的模式|
|domain|返回装载文档所在的服务器域名|
|lastModified|返回文档的最后修改日期和时间|
|readyState|返回文档的载入状态|
|referrer|返回装载当前文档的URL|
|title|设置或返回文档的标题|
|URL|返回文档的完整网址|

* document的对象方法

|方法|描述|
|:---|:---|
|close()|关闭以前用document.open()打开的输出流|
|getElementById()|访问第一个指定id的元素|
|getElementsByName()|访问所有指定name的元素|
|getElementsByTagName()|访问所有指定tagname的元素|
|open()|打开一个输出流，以便收集document.write()或document.writeln()的输出|
|write()|将HTML表达式或js代码写入文档|
|writeln()|与write()相同，但是在每条语句后添加一个换行字符|

* getElementById()方法和innerHTML属性
```
# 获得document中id=idtest的第一个元素
var d = document.getElementById('idtest')
# d的HTML内容
d.innerHTML
```

* open()和close()
```
# open() 打开新链接
window.open(URL, name, specs, replace)
# close()，关闭已打开的窗口，只能关闭由脚本打开的窗口。