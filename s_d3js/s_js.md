## 常用命令
```
typeof <varname>; // 查看变量类型
window; // 在浏览器中是一个顶级对象，包含所有JS中能直接访问到的对象。
.attr("class", "bar");  // 添加class="bar"
.classed("bar", true);  // 给选中的元素添加类bar, false时则是删除类bar
.style(height,"70 px");   // 给选中的元素添加style属性，例中值为 style="height:70 px"
```

## 变量赋值
var amount = 200;
defaultColor = 'hot pink';
var t = true;

## 查看变量类型
```
typeof amount;
```
## 数组
```
var numbers = [5,10,15,20,25];
numbers[2] //数组下标从0开始，返回15
```
## 对象(字典)
```
var fruit = {
    kind: 'grape',
    color: 'red',
    quantity: 12,
    tasty: true
};
fruit.kind  // 引用对象中的某个值
```
## GeoJSON, 是基于JSON的一种格式，专门用于保存地理数据。
```
{
    "type": "FeatureCollection",
    "features":[
        {
            "type": "Feature",
            "geometry":{
                "type": "Point",
                "coordinates": [150.1282427, -24.471803]
            },
            "properties":{
                "type": "town"
            }
        }
    ]
}
```


## js中的加+,减-,乘*, 除 /
## js中的比较
```javaScript
    == 等于
    != 不等于
    <, <=  小于,小于等于
    >, >=
```

## js 中的控制结构
```
    // if(){}
    if (3 <5 >) {
        console.log(" Eureka! Three is less than five!");
    }
    // for () {}
    for (initialization; test; update){
        expression;
    }
    for (var i = 0; i < 5; i++){
        console.log(i);
    }
```
```
    // 使用for()对数组做遍历
    var numbers = [1, 3, 5, 7, 9, 11, 13]
    for (var i = 0; i < numbers.length; i++){
        console.log(numbers[i])
    }
```

## 自定义函数
```
var calculateGratuity = function(bill){
    return bill*0.2;
}
```

## 引用脚本文件
```
<body>
    <script type="text/javascript">
        alert("Hello, world!");
    </script>
</body>
```
```
<head>
    <script type="text/javascript" src="myscript.js">
    </script>
</head>
```

# SVG, Scalable Vector Graphics, 可伸缩矢量图形。
## SVG创建简单的圆形
```
<svg width="50" height="50">
    <circle cx="25" cy="25" r="22" fill="blue" stroke="grey" stroke-width="2"/>
</svg>
```
## SVG中可以嵌入的可见元素，包括rect, circle, ellipse, line, text, path
```
<svg width="500" height="50">
    <rect x="0" y="0" width="500" height="50"/>
</svg>
```
```
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <!-- circle, 绘制圆形, cx和cy指定圆心坐标, r指定半径 -->
        <svg width="500" height="50">
            <circle cx="250" cy="25" r="20" fill="blue" stroke="gray" stroke-width="2"/>
        </svg>
        </br>
        <!-- rect, 绘制矩形, x和y指定矩形左上角的坐标点, width和height指定宽高 -->
        <svg width="500" height="50">
            <rect x="0" y="0" width="500" height="50"/>
        </svg>
        </br>
        <svg width="500" height="500">
            <!-- ellipse, 绘制椭圆形, 与circle类似, rx和ry分别指定半径 -->
            <ellipse cx="250" cy="25" rx="100" ry="25"/>
            <!-- line, 绘制直线, x1 y1指定起点坐标, x2 y2指定终点坐标, 必须用stroke指定直线颜色 -->
            <line x1="0" y1="50" x2="500" y2="100" stroke="black"/>
            <!-- text, 绘制文本, x指定文本左上角的位置, y指定字体的基线位置 
                 SVG文本会继承CSS为父元素指定的字体样式
            -->
            <text x="250" y="125">SVG text 文本绘制演示，注意yp字符与基线的位置</text>
            <!-- text, 指定样式 -->
            <text x="250" y="150" font-family="serif" font-size="25" fill="red">SVG text</text>
        </svg>
    </body>
</html>
```
## SVG常见属性
* fill, 填充色，可使用颜色名, 十六进制值, 或RGB  RGBA值
* stroke 线条颜色
* stroke-width 线条宽度
* opacity 透明度，0.0-完全透明，1.0-不透明
* font-family  字体
* font-size  字体大小

## SVG遮挡和透明度
```
<!-- 最后绘制的SVG图形会盖住之前绘制的图形，
     rgba()接受0到255之间的三个RGB色值，还可以接受0.0-1.0之间的透明度值。
-->
<svg width="500" height="500">
    <circle cx="25" cy="25" r="20" fill="rgba(128,0,128,1.0)"/>
    <circle cx="50" cy="25" r="20" fill="rgba(0,0,255, 0.75)"/>
    <circle cx="75" cy="25" r="20" fill="rgba(0,255,0, 0.5)"/>
    <circle cx="100" cy="25" r="20" fill="rgba(255,255,0, 0.25)"/>
    <circle cx="125" cy="25" r="20" fill="rgba(255,0,0, 0.1)"/>
</svg>
<!-- 对已经使用了rgba()设置透明色的元素应用opcity属性, 透明值会相乘  -->
<svg width="500" height="100">
    <circle cx="25" cy="25" r="20" fill="rgba(128,0,128, 0.75)" stroke="rgba(0,255,0, 0.25)" stroke-width="10"/>
    <circle cx="65" cy="25" r="20" fill="rgba(128,0,128, 0.75)" stroke="rgba(0,255,0, 0.25)" stroke-width="10" opacity="0.5"/>
    <circle cx="105" cy="25" r="20" fill="rgba(128,0,128, 0.75)" stroke="rgba(0,255,0, 0.25)" stroke-width="10" opacity="0.2"/>
</svg>

```

# 数据加载
## d3.csv("csvfile", function(data){})  异步方法，加载csv文件
```
var dataset;
d3.csv("food.csv", function(error, data) {
    if (error) { // 如果 error 不是 null，肯定出错了
        console.log(error); // 输出错误消息
    } else { // 如果没出错，说明加载文件成功了
        console.log(data); // 输出数据
        // 包含成功加载数据后要执行的代码
        dataset = data;
        generateVis();
        hideLoadingMsg();
    }
});
```
## d3.tsv() 加载tsv文件
## d3.json()  加载JSON数据

## .enter() 选择不存在的元素
```
de.select("body").selectAll("p")
    .data(dataset)
    .enter()
    .append("p")
    .text("New paragraph!");
```

