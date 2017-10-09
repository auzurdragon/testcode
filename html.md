
# 在p标签内换行

## 英文换行
```HTML
Div p{ word-break:break-all; width:150px;}  /*只对英文起作用，以字母作为换行依据*/
Div p{ word-wrap:break-word; width:150px;}  /*只对英文起作用，以单词作为换行依据*/
```
*注意有的时候英文单词是一个整体不能拆开！！！*

## 中文换行
```HTML
Div p{white-space:pre-wrap;width:150px;}/*只对中文起作用，强制换行*/
Div p{white-space:nowrap;width:10px;}/*强制不换行，都起作用*/
```

## 强制不换行以及超出宽度部分文字隐藏
```HTML
.p5{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:100px;}／/*不换行，超出部分隐藏且以省略号形式出现*/
```
*一定要注意div或者p标签里面要有一个宽度才可以换行，要不然没有作用*

## 其它参数
>normal:依照亚洲语言和非亚洲语言的文本规则，允许在字内换行  
>break-all:该行为与亚洲语言的normal相同。也允许非亚洲语言文本行的任意字内断开。该值适合包含一些非亚洲文本的亚洲文本  
>keep-all:与所有非亚洲语言的normal相同。对于中文，韩文，日文，不允许字断开。适合包含少量亚洲文本的非亚洲文本