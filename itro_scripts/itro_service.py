# -*- coding=utf-8 -*-
"""
依赖包
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymongo, redis
time, bson
pywin32：需要下载安装，不能使用PIP，http://sourceforge.net/projects/pywin32/files/pywin32/

安装服务
python itro_service.py install
让服务自动启动
python itro_service.py --startup auto install
启动服务
python itro_service.py start
重启服务
python itro_service.py restart
停止服务
python itro_service.py stop
删除/卸载服务
python itro_service.py remove
"""
import win32serviceutil
import win32service
import win32event

class itro_service(win32serviceutil.ServiceFramework):
    """配置服务"""
    _svc_name_ = "itroService"
    _svc_display_name_ = "itroService"
    _svc_description_ = "itro项目服务：1.处理经销商进货系统中的已收货订单付款；2.处理缓存中已领取的红包记录；3.删除高德云上过期的红包记录。脚本和日志记录：/itrolog/ 。基于python 3.6.1 和 pywin32，依赖包: pymongo, redis"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.isAlive = True

        self.mongo = {
            'HOST':'localhost',
            'PORT':28010,
            'DBMain':'iTROdb',
            'DBFlow':'iTROLogdb',
            'DBSocial':'iTRO_SocialDb',
            'COPurchase':'iTRO_Purchase',
            'COStore':'iTRO_Store',
            'COUser':'iTRO_User',
            'COFlow':'iTRO_FlowLog',
            'CORed':'iTRO_RedPacket',
            'COError':'iTRO_redError',
        }
        self.redis = {
            'HOST':'localhost',
            'PORT':6394,
            'DB':0,
            'HKEY':'RedrainGetPirce'
        } 

    def _getLogger(self):
        import logging
        import os
        import inspect

        # 获得一个logging实例
        logger = logging.getLogger("[itroService]")
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "service.log"))
        # 设置日志记录的格式
        formatter = logging.Formatter("%(asctime)s %(name) - 12s %(levelname) -8s %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        import time
        from itro_purchasepay import do_purchasepay
        from itro_amapred import amap_redpacket
        from itro_redpacket import itro_redpacket
        from itro_scriptall import to_flowlog

        self.logger.error("svc do run....")
        while self.isAlive:
            time.sleep(60)
        # 服务1：处理经销商进货表中已付款收货且15天未支付的订单，即15天自动付款。
            # 依赖脚本 from itro_purchasepay import do_purchasepay
            # 依赖脚本 from itro_scriptall import to_flowlog
            # 只在凌晨1点期间执行本任务，gmtime()的时间比北京时间要晚8小时
            if time.gmtime().tm_hour == 9:
                svcPurchase = do_purchasepay(self.mongo)
                svcPurchase.get_paylist()
                svcPurchase.get_nid()
                for i in svcPurchase.result:
                    tmp = svcPurchase.do_addmoney(nid=i["nid"], amount=i["amount"])
                    if tmp:
                        i["userid"] = tmp["userid"]
                        i["remain"] = tmp["usemoney"] + i["amount"]
                    else:
                        i["log"] = "do_addmoney failed"
                        logmsg = "%s purchaseid do_addmoney failed" % (i["purchaseid"].__str__())
                        self.logger.error(logmsg)
                        continue
                    tmp = svcPurchase.upd_paylog(i["purchaseid"])
                    if tmp:
                        try:
                            to_flowlog(mongo={"HOST":self.mongo["HOST"],
                                              "PORT":self.mongo["PORT"],
                                              "DB":self.mongo["DBflow"],
                                              "CO":self.mongo["COFlow"]},
                                       userid=i["userid"], orderid=i["orderid"], ordertype=2,
                                       logtype=10602, amount=i["amount"], remain=i["remain"],
                                       memo="商家进货付款", logtype2=0, goldtype=3)
                        except:
                            logmsg = "%s purchaseid to_flowlog failed" % i["purchaseid"].__str__()
                            self.logger.error(logmsg)
                    else:
                        i["log"] = "upd_paylog failed"
                        logmsg = "%s purchaseid upd_paylog failed" % i["purchaseid"].__str__()
                        self.logger.error(logmsg)
                if len(svcPurchase.result) > 0:
                    logmsg = "%d purchaseid have done" % len(svcPurchase.result)
                    self.logger.info(logmsg)

        # 服务2：清理高德云数据库中的过期红包记录
            svcAmapred = amap_redpacket()
            try:
                svcAmapred.get_redpacket()
                t = svcAmapred.del_redpacket()
                logmsg = "高德云图红包记录处理，%d redpacketlogs have done" % t
                # self.logger.info(logmsg)  # 记录处理成功记录，关闭
            except:
                logmsg = "高德云图红包记录处理，del_redpacket has errors"
                self.logger.error(logmsg)

        # 服务3：清理redis缓存中的领取红包记录，给相应的账号加钱。
            svcRedpacket = itro_redpacket(mongo=self.mongo, redis=self.redis)
            if svcRedpacket.get_redField():
                for i in svcRedpacket.result:
                    try:
                        svcRedpacket.get_redValue(i)
                        # 0915：延迟2秒执行，分散服务器压力
                        time.sleep(2)
                        svcRedpacket.get_userRemain(i)
                        svcRedpacket.to_userRemain(i)
                        svcRedpacket.to_redlog(i)
                        svcRedpacket.del_redlog(i)
                        to_flowlog(
                            mongo={"HOST":self.mongo["HOST"],
                                   "PORT":self.mongo["PORT"],
                                   "DB":self.mongo["DBFlow"],
                                   "CO":self.mongo["COFlow"]},
                            userid=svcRedpacket.result[i]["getuid"],
                            orderid='red'+str(int(time.time())),
                            ordertype=2,
                            logtype=10501,
                            amount=svcRedpacket.result[i]['val'],
                            remain=svcRedpacket.result[i]['remain'],
                            memo="红包",
                            logtype2=0,
                            goldtype=3
                            )
                    except Exception as e:
                        logmsg = "红包缓存，rkey %s 处理报错 %s " % (svcRedpacket.result[i]["rkey"] , e.__str__())
                        self.logger.error(logmsg)
                        svcRedpacket.to_errorlog(i)
                logmsg = "红包缓存处理： %d 条记录处理完成" % svcRedpacket.lognum
                self.logger.info(logmsg)

        # 等待服务停止
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        # 通知SCM停止过程
        self.logger.error("svc do stop...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(itro_service)

