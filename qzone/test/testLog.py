#coding:utf8
'''
Created on 2016年7月15日

@author: wb-zhaohaibo
'''


import logging


logger = logging.getLogger()
handler = logging.FileHandler("logger_test.txt")
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)#日志输出级别


logger.error("test error!")
logger.warn("test warn!")
logger.info("test info!")
try:
    1/0
except Exception as e:
    logger.error(e)