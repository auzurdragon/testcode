"""
    使用itro_redpacket包，从redis中读取红包记录
    将记录写入到iTRO_User, iTRO_RedPacket, iTRO_FlowLog表。
    完成操作后, 从redis中删除对应记录，并保存日志文件在e:/itrolog
"""
from itro_redpacket import iTRO_redPacket
t = iTRO_redPacket()
t.do_redpacket()
