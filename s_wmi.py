#coding:utf-8

"""
    使用wmi监控windows服务
    依赖包：wmi，下载地址 http://mirrors.aliyun.com/pypi/simple/wmi/
    安装方法：1.下载wmi并解压; 2.在下载目录下执行  python setup.py install
    依赖包：psutil
"""

import wmi

# 创建对象
c = wmi.WMI()
# 查看wmi方法
c._get_classes()

c.Win32_OperatingSystem()[0].Caption    # 获得操作系统版本
c.Win32_OperatingSystem()[0].OSArchitecture # 获得操作系统的位数
c.Win32_OperatingSystem()[0].NumberOfProcesses  # 当前系统运行的进程总数

c.Win32_Processor()[0].Name # CPU类型
c.Win32_PhysicalMemory()[0].Capacity    # 内存大小


# 获得进程列表
c.Win32_Process()
c.Win32_process()[0]._getAttributeNames()   # 获得进程的属性名称

# 获得服务列表
c.Win32_Service()

# 静态信息
OS信息：Win32_OperatingSystem()
Disk信息：Win32_LogicalDisk()
Mem信息：Win32_CompiterSystem()
CPU信息：Win32_Processor()
Net信息：Win32_NetworkAdapterConfiguration()


# 动态信息psutil
import psutil as ps

# 查看CPU所有信息
ps.cpu_times()
ps.cpu_times(percpu=True)   # 显示cpu的逻辑信息
ps.cpu_times().user         # 查看用户的CPU时间比
ps.cpu_count()              # CPU的核心个数

# 查看内存信息
ps.virtual_memory()         # 内存的所有信息
ps.virtual_memory().total   # 总计内存
ps.virtual_memory().used    # 已使用内存
ps.virtual_memory().free    # 空闲内存

# 查看交换内存信息
ps.swap_memory()

# 查看磁盘信息
ps.disk_io_counters()       # 查看磁盘IO信息
ps.disk_partitions()        # 磁盘完整信息
ps.disk_useage("/")         # 查看分区表参数
ps.disk_io_counters(perdisk=True)   # 获取单个分区IO个数

# 查看网络信息
ps.net_io_counters()        # 查看网络总IO信息
ps.net_io_counters(pernic=True)     # 每个接口信息

# 当前登录用户的登录信息
ps.users()

# 开机时间
ps.boot_time()

# 系统进程管理
ps.pids()       # 查看全部进程
ps.Process(<pid>)   # 查看单个进程
.name()     # 进程名
.exe()      # 进程的bin路径
.cwd()      # 进程的工作目录路径
.status()   # 状态
.create_time()  # 创建时间
.uids()     # uid信息
.gids()     # gid信息
.cpu_times()    # cpu时间信息，包括user,system
.cpu_affinity() # cpu亲和度
.memory_percent()   # 内存使用率
.memory_info()      # 内存信息，rss,vms
.io_counters()      # IO信息
.connectios()       # 进程列表
.num_threads()      # 开启的线程数
.as_dict(attrs=['name','pid'])  # 将attrs中的值转成dict

ps.process_iter()   # 创建一个遍历所有进程的迭代器
ps.win_service_iter()   # 创建一个遍历所有服务的迭代器

ps.win_service_get("sername")   # 按服务名称检索服务，检索不到返回 psutil.NoSuchProcess 错误
.as_dict()              # 以dict形式输出服务的信息
.binpath()              # 运行文件路径
.description()          # 服务的描述
.display_name()         # 服务显示的名称
.name()                 # 服务名称
.pid()                  # 服务的PID，未启动的服务pid为None
.start_type()           # 启动类型
.status()               # 服务状态
.username()             # 用户名称

# 跟踪程序相关信息
from subprocess import PIPE
p = ps.Popen("/usr/bin/python", "-c" "print('hello')",stdout=PIPE)
p.name()
p.username()


# 示例：监控指定服务的进程资源占用
servicename = [""]