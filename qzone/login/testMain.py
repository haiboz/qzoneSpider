#coding:utf8
'''
Created on 2016-6-24

@author: 浮生若梦
'''

import sqlConnect
from qzone.spiderUtils import qqParser
# 
parser = qqParser.QQParser()
qq = "1069757861"
parser.parseMood(qq)
connect = sqlConnect.SQLConnect()
# conn = connect.connect()
# cursor = conn.cursor()
content = "content"
date = "2016-01-02"
scount = "2"
pcount = "3"
zcount = "5"
sql = "insert into mood(mood_id,date,mood_content,support_count,comment_count,forward_count) values('"+qq+"','"+date+"','"+content+"',"+scount+","+pcount+","+zcount+")" 
# connect.insert(sql)


# try:
#     cursor.execute(sql)
#     conn.commit()
#     print "insert 成功"
# except Exception as e:
#     print e
#     conn.rollback()
# cursor.close()
#conn.close()


# 
# s1="赞(ss"
# s2="("
# if s2 in s1:
#     print "ssss"
# else:
#     print "tttt"

