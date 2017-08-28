"""
    使用itro_redpacket包，从redis中读取红包记录
    将记录写入到iTRO_User, iTRO_RedPacket, iTRO_FlowLog表。
    完成操作后, 从redis中删除对应记录，并保存日志文件在e:/itrolog
"""
import itro_redpacket
T = itro_redpacket.iTRO_redPacket()
T.get_redLog()
for i in range(len(T.RESULT)):
    T.get_userRemain(i)
    T.to_userRemain(i)
    T.to_redlog(i)
    T.to_flowlog(i)
    T.del_redlog(i)
T.to_logfile()
