#coding:utf-8
"""
    统计服务器总体资源占用情况和监控指定进程的资源占用
    1. 依赖：pywin32, psutil。
    2. 日志保存位置，与脚本路径相同。
    3. 每分钟统计一次。
    
"""
import win32serviceutil
import win32service
import win32event
import time
import psutil as ps

class itro_cpustat(win32serviceutil.ServiceFramework):
    _svc_name_ = "itroCPUStat"
    _svc_display_name_ = "itroCPUStat"
    _svc_description_ = "脚本位置：itro_scripts/itro_cpustat.py。记录位置：itro_scripts/cpustat.log。监控CPU内存资源占用情况，监控IIS,MongoDB,Redis,itroservice,automaticreceiptservice服务的资源占用。每分钟记录一次"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.isAlive = True
        self.servname = ["IISADMIN", "MongoDB", "Redis", "itroService","AutomaticReceiptService"]

    def _getLogger(self):
        import logging
        import os
        import inspect

        # 获得一个logging实例
        logger = logging.getLogger("[cpustat]")
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "cpustat.log"))
        # 设置日志记录的格式
        formatter = logging.Formatter("%(asctime)s %(name) - 12s %(levelname) -8s %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        self.logger.error("svc do run....")
        while self.isAlive:
            time.sleep(10)
            servinfo = []
            for i in self.servname:
                # 判断服务是否存在
                try:
                    t = ps.win_service_get(i)
                    # 判断服务是否启动
                    if t.status() == "running":
                        servinfo.append({
                            "name":i,
                            "status":t.status(),
                            "pid":t.pid(),
                        })
                    # 服务未启动
                    else:
                        msg = "error:servicd %s status: %s" %(i, t.status())
                        self.logger.error(msg) 
                # 服务不存在
                except ps.NoSuchProcess as errors:
                    msg = "error:have no service $s" % i
                    self.logger.error(msg)
            # 查询进程的资源占用
            for i in servinfo:
                proc = ps.Process(i["pid"])
                procname = proc.name()
                procpid = proc.pid
                procstatus = proc.status()
                cpu_percent = proc.cpu_percent(interval=1)
                memory_percent = proc.memory_percent()
                msg = "pid:%d|service:%s|process:%s|status:%s|cpu:%.2f|memory:%.2f " % (procpid, i["name"], procname, procstatus, cpu_percent, memory_percent)
                self.logger.info(msg)
            # 查询系统的总体资源占用
            cpu_percent = ps.cpu_percent()
            memory_percent = ps.virtual_memory().percent
            msg = "service:total|cpu:%.2f|memory:%.2f" % (cpu_percent, memory_percent)
            self.logger.info(msg)

    def SvcStop(self):
        # 通知SCM停止过程
        self.logger.error("svc do stop...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(itro_cpustat)
