# CSS
## CSS样式
```
    选择符A {
        属性:值;
        属性:值;
        属性:值;
    }
```
设置p和li为相同的文字大小、行高和颜色
```
    p,
    li {
        font-size: 12px;
        line-height: 14px;
        color: orange;
    }
```
## CSS选择符
* 类型选择符
    * h1  /* 选择所有一级标题 */
    * p   /* 选择所有段落   */
* 后代选择符：匹配包含在另一个元素中的元素
    * h1 em   /* 选择包含在h1中的em元素    */
    * div p   /* 选择包含在div中的p元素    */
* 类选择符：匹配具有指定类class的所有元素
    * .caption    /* 选择带有'caption'类的元素    */
    * .label      /* 选择带有'label'类的元素      */
    * .bar.highlight  /* 多个类, 选择高亮(hightlight)和条形(bar)    */
* id 选择：匹配具有给定ID的一个元素（一个ID只能在DOM中出现一次)
    * #header /* 选择id为'header'的元素  */
    * #nav    /* 选择id为'nav'的元素     */
* 组合选择
    * div.sidebar /* 只选择带有'sidebar'类的div   */
    * #button.on  /* 只选择带有'on'类，且id为'button'的元素   */

## CSS 注释
    /* 注释内容 */

## CSS 引用
1. 在HTML中嵌入CSS, 在head style 中嵌入
```
<head>
    <style type="text/css">
        p {
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
```
2. 在HTML中引用外部样式表
```
<head>
    <link rel='stylesheet' href='style.css'>
    <!-- rel属性指示被链接的文档是一个样式表
         href 指定被链接的文档位置
         type 指定被链接文档的MIME类型
     -->
</head>
```
3. 插入行内样式
```
<p style="color: blue; font-size: 48px; font-style:italic;">
    Inline styles are kind of a hassle
</p>
```