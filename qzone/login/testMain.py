#coding:utf8
'''
Created on 2016-6-24

@author: 浮生若梦
'''

import sqlConnect
from qzone.spiderUtils import qqParser
from qzone.login import login
import qZoneMain
# 
class TestMain(object):
    def __init__(self):
        self.parser = qqParser.QQParser()
        self.qZoneMain = qZoneMain.QQMain()
        self.sqlConnect = sqlConnect.SQLConnect()
        self.login = login.QZoneLogin()
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

    
    def testInsertQQ(self, qq):
        self.qZoneMain.insertDealtQQ(qq)
        pass

    
    def testInsertSpicelSignl(self):
        '''测试sql插入特殊字符'''
        content = "it's 自动释放 or never"
#             content = content.replace("'", "\\'")
        sql = "insert test(content) values ('"+content+"')" 
        self.sqlConnect.insert(sql)
        print "success"
        pass

    
    def testGetLoginQQ(self):
        count = 1
        while count < 10:
            qq,pwd = self.login.getInitInfo(count)
            print qq
            print pwd
            count = count + 1
        
        pass
    
    
    
if __name__ == "__main__":
        testMain = TestMain()
#         
#         testMain.testIns()
#         testMain.testParseQQFrind()
#         testMain.testInsertQQ("798102408")
#         testMain.testInsertSpicelSignl()
        testMain.testGetLoginQQ()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
