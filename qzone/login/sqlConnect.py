# coding:utf8
'''
Created on 2016-6-24

@author: 浮生若梦
'''

import MySQLdb
print MySQLdb
import codecs


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
            open("log_error.log","a+").write("select error:sql = "+sql+"\n")
            print "查询异常sql:"+sql
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
            open("log_error.log","a+").write("insert error:sql = "+error+"\n")
            print "插入异常:sql="+sql
            print e
#         cursor.close()
#         conn.close()
            
        
        