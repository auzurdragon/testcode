# -*- coding=utf-8 -*-

import logging


# 将日志输出到控制台
logging.basicConfig(level=logging.WARNING,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:%(message)s"
)

logging.info("info message")
logging.debug("debug message")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")

# 将日志输出到文件
logging.basicConfig(level=logging.WARNING,
    filename='./log/log.txt',
    filemode='w',
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
)
