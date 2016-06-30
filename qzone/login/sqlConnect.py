# coding:utf8
'''
Created on 2016-6-24

@author: 浮生若梦
'''

import MySQLdb
print MySQLdb


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
    
    def insert(self,sql):
        '''插入语句'''
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            self.dualSelect()
            print "插入成功"
        except Exception as e:
            print "插入失败:sql="+sql
            print e
#         cursor.close()
#         conn.close()
            
        
        