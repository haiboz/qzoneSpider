# coding:utf8
'''
Created on 2016-6-24

@author: 浮生若梦
'''

import MySQLdb
print MySQLdb
from qzone.spiderUtils import commonUtils

class SQLConnect(object):
    def __init__(self):
        self.conn = MySQLdb.Connect(
                               host="127.0.0.1",
                               port=3306,
                               user="user",
                               passwd="user",
                               db="qqspider",
                               charset="utf8"
                       )

    def connect(self):
        return self.conn
    
    def dualSelect(self):
        '''空查询'''
        sql = "select 1 from dual"
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close() 
    
    def select (self,sql):
        '''查询sql 返回cursor对象'''
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except :
            localTime = commonUtils.CommonUtils().getLocalTime()
            open("log_error.log","a+").write(localTime+" select error:sql = "+sql+"\n")
        return cursor    
    
    def insert(self,sql):
        '''插入语句'''
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            self.dualSelect()
        except Exception as e:
            error = sql.encode("utf-8")
            localTime = commonUtils.CommonUtils().getLocalTime()
            open("log_error.log","a+").write(localTime+" insert error:sql = %s \nException: %s\n" % (error,e))
            
        
        