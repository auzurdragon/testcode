# -*- coding=utf-8 -*-

import win32serviceutil
import win32service
import win32event
import os
import logging
import inspect

class PythonService(win32serviceutil.ServiceFramework):
    # 服务名
    _svc_name_ = "PythonService"
    # 服务显示名称
    _svc_display_name_ = "Python Service Demo"
    # 服务描述
    _svc_description_ = "Python Service Demo"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.run = True

    def _getLogger(self):
        logger = logging.getLogger("[PythonService]")
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = loggin.FileHandler(os.path.join(dirpath, 'service.log'))

        formatter = logging.Formatter('%(asctime)s %(name) - 12s %(levelname) -8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger
    
    def SvcDoRun(self):
        from time import time
        print(int(time()))
        # 等待服务被停止
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
    
    def SvcStop(self):
        # 告诉SCM停止这个过程
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(PythonService)