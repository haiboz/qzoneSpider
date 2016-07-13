# coding:utf8
'''
Created on 2016-7-12

@author: 浮生若梦
'''
import time

class CommonUtils(object):
    
    def getLocalTime(self):
        '''获取当地格式化后的时间'''
        ISOTIMEFORMAT="%Y-%m-%d %X"
        localtime = time.strftime( ISOTIMEFORMAT, time.localtime() )
        return localtime
    
    def waitWebLoad(self,browser):
        '''判断页面是否加载完成'''
        pass


