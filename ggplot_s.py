# 安装ggplot，需要numpy, scipy支持，安装过程容易报错
# 升级pip, 以免安装.whl失败。注意 .whl文件名不能修改，不要使用迅雷下载
# pip install --upgrade setuptools

# 安装numpy,scipy，windows下需要编译，可以在http://www.lfd.uci.edu/~gohlke/pythonlibs/ 下载编译包.whl安装。
# pip install .whl

# windows下需要安装VC++ 14.0，http://landinghub.visualstudio.com/visual-cpp-build-tools ，在该网站下载 Visual C++ Build Tools 2015 

# 安装ggplot
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ggplot

# 绘制散点图
import ggplot as gp
meat = gp.meat	# 使用ggplot自带的测试数据
p = gp.ggplot(
    gp.aes(
        x='date',   # 指定x轴数据
        y = 'beef', # 指定y轴数据
        color='beef'),  # 指定填充颜色
    data = meat)    # 指定数据集

p +gp.geom_line()  # 绘制折线图
p + gp.geom_point() # 绘制散点图

# 绘制分面图
gp.ggplot(gp.aes(x = 'carat', y = 'price', color = 'color'), data = gp.diamonds) + gp.geom_point() + gp.facet_wrap('cut')

# 绘制直方图
gp.ggplot(gp.aes(x = 'price'), data = gp.diamonds) + gp.geom_histogram()