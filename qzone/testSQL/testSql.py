# coding:utf8
'''
Created on 2016-7-1

@author: 浮生若梦
'''
import time
from qzone.login import sqlConnect 
startTime = time.time()
print "开始时间：%d" % startTime
connect = sqlConnect.SQLConnect()
conn = connect.connect()
cursor = conn.cursor()

i = 1000000
while i < 2000000:
    sql = " insert into testqq(qq) values(%d)" % i
    cursor.execute(sql)
    i = i + 1
conn.commit()


# i = 7872932
# sql = "select qq from testqq where qq = %d" % i
# cursor.execute(sql)
# print "记录数：%d " % cursor.rowcount
cursor.close()
conn.close()
endTime = time.time()
print "结束时间：%d" % endTime
print "共耗时 %d 秒！" % (endTime - startTime)






