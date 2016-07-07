#coding:utf8
'''
Created on 2016-6-24

@author: 浮生若梦
'''

import sqlConnect
from qzone.spiderUtils import qqParser
# 
class TestMain(object):
    def __init__(self):
        self.parser = qqParser.QQParser()
        self.qq = "1069757861"
    
    
    
    def testIns(self):
        qq = self.qq
        self.parser.parseMood(qq)
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
        
        
    def testParseQQFrind(self):
        print "testParseQQFrind"
        self.parser.parseQQFriend(self.qq)
        
        
        
    
if __name__ == "__main__":
        testMain = TestMain()
#         testMain.testIns()
        testMain.testParseQQFrind()
