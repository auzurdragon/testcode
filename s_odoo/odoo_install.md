# odoo介绍
odoo, 原名openERP，是开源的ERP系统。使用python和js开发。
[odoo官网](https://www.odoo.com/zh_CN/)
[安装说明](https://www.odoo.com/documentation/11.0/setup/install.html)

OenpERP（已更名为odoo）是一个开源的ERP框架，主要特点：
* 开源，开源，开源！
* B/S架构
* Python和JavaScript开发
* 可以在Windows或Linux上运行。如果需要进行二次开发的话，最好使用Linux
* 架构灵活，所有模块都可以根据需要安装和卸载，

> 参考：[odoo官网](https://www.odoo.com/zh_CN/)  
> 参考：[官网安装说明](https://www.odoo.com/documentation/11.0/setup/install.html)

# 注意事项
*  环境：阿里云CentOS7.4+Python2.7.14
* 坑：CentOS自带的Python版本为2.7.5，在安装Python2.7.14时，一定要注意避免冲突，不然会多出很多莫名其妙的问题。
* 坑：之前没用过postgresql，不知道是切换用户以后启动odoo，才能让odoo调用postgresql，这处尝试了好久。。。。
* 坑：安装odoo所需要的python环境时，会出现找不到***文件的错误，安装相应的软件包即可。
另外，在注册页面可以选择中文。还有感觉运行速度很慢，不知道是不是免费主机的原因。

# 预先准备
* python2.7.14，CentOS7.4自带的Python是2.7.5，所以安装时要避免冲突。
```
# 安装Python前需要的软件包
yum install sqlite-devel bzip2-devel ncurses-devel openssl-devel gcc

# 备份原有的python2.7.5文件
cp /usr/bin/python2.7 /usr/bin/python2.7.5

# 安装python2.7.14到opt目录
mkdir -p /opt/python/2.7.14/lib
cd /tmp/Python-2.7.14
./configure --enable-shared --prefix=/opt/python/2.7.14 LDFLAGS="-Wl,-rpath /opt/python/2.7.14/lib"
# --enable-shared，标记生成动态链接库
# --prefix, 指定安装目录
# LDFLAGS, 将生成的库文件放到指定目录中
make && make install && make clean
```
* 安装pip
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
* virtualenv，python环境管理工具  
odoo可指定python，所以不安装也可以。推荐安装
```
pip install virtualenv
mkdir /var/pythonenv
cd /var/pythonenv
virtuanenv --python=/opt/python/2.7.14/bin/python --no-site-packages python2_odoo
# no-site-packages, 表示不使用系统库中的packages，以保持一个干净的环境

# 激活python2.7.14环境
cd python2_odoo
source bin/activate
deactivate

# 修改默认的python版本，注意备份
mv /usr/bin/python2.7 /usr/bin/python2.7.5
ls -s /opt/python/2.7.14/bin/python /usr/bin/python
```
* 修改yum配置  
安装python后，必须修改 /usr/bin/yum 和 /usr/libexec/urlgrabber-ext-down 中的python指向原2.7.5，否则yum会报错
`#! /usr/bin/python2.7.5`

# 安装postgresql, odoo使用此数据库
```
yum install -y postgresql
systemctl enable postgresql # 设置开机启动
systemctl start postgresql  

# PostgreSQL 安装完成后，会建立一下‘postgres’用户，用于执行PostgreSQL。
su - postgres  # 切换用户
psql -U postgres # 登录数据库
ALTER USER postgres WITH PASSWORD '123456' # 修改用户密码
\q  # 退出数据库
exit  # 巡出psql命令行

systemctl restart postgresql
```
# 安装nodejs
不安装也能运行，但启动以后登录到odoo会加载不了样式，提示`Could not execute command 'lessc'`  
```
yum install -y nodejs
npm install -g less
```

# 安装odoo
  因为使用的是zip安装，直接下载后解压即可，无需要编译
```
# 安装所需要的软件包，否则在之后安装python packages时会报错
yum install -y python-devel libxml2-devel libxslt-devel openldap-devel

# 解压到 /var/odoo/ 目录 ，过程略
cd /var/odoo
# 安装odoo所需要的packages
pip install -r requirements.txt
```

# 启动odoo
```
# 修改odoo-bin，将python链接指向环境
# 启动postgresql环境
su - postgres   # postgres 是之前安装postgresql时默认创建的用户名
# 启动odoo
cd /var/odoo
./odoo-bin
```
> 启动成功后，使用浏览器访问 localhost:8069, 出现odoo注册页面即启动成功。