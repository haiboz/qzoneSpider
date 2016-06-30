#coding:utf8
'''
Created on 2016-6-24

@author: 浮生若梦
'''
from bs4 import BeautifulSoup
from qzone.login import sqlConnect

class QQParser(object):
    '''解析器'''
    def __init__(self):
        self.connect = sqlConnect.SQLConnect()
        pass
    
    def parseMood(self,currentQQ):
        '''解析说说信息并保存数据库'''
        cont = open("page_shuoshuo.html","r+").read()
        soup = BeautifulSoup(cont,"html.parser",from_encoding="utf-8")
        #<ol id="msgList"   说说内容
        moodTag = soup.find("ol",id = "msgList")
        liTag = moodTag.find_all("li",class_="feed")
        index = 0
        sql = ""
        for li in liTag:
            mood=""
            date=""
            support=""
            comment=""
            foward=""
            
            #说说内容
            moodTags = li.find_all("pre",style="display:inline;")
            if moodTag is None:
                mood = ""
            else:
                mood = ""
                for moodTag in moodTags:
                    mood = mood + moodTag.get_text()+"//"
                mood = mood[:-2]
            print mood
            #发表日期
            dateTag = li.find("a",attrs={'class':'c_tx c_tx3 goDetail'})
            if dateTag is None:
                date = ""
            else:
                date = dateTag.get_text()
            print date
            #点赞人数
            supportTag = li.find("a",style="display: inline-block;",attrs={'class':'qz_like_btn c_tx mr8'})
            if supportTag is None:
                support = "0"
            else:
                support = supportTag.get_text()
                if "(" in support:#赞(1)
                    support = support[2:-1]
                else:
                    support = "0"
            print "赞："+support
            #评论人数
            commentTag = li.find("a",attrs={'class':'c_tx comment_btn'})
            if commentTag is None:
                comment = "0"
            else:
                comment = commentTag.get_text()
                if "(" in comment:#评论(1)
                    comment = comment[3:-1]
                else:
                    comment = "0"
            print "评论："+comment
            #转发人数
            fowardTag = li.find("a",attrs={'class':'c_tx forward_btn'})
            if fowardTag is None:
                foward = "0"
            else:
                foward = fowardTag.get_text()
                if "(" in foward:#转发(1)
                    foward = foward[3:-1]
                else:
                    foward = "0"
            print "转发："+foward
            index = index + 1
            sql = "insert into mood(mood_id,date,mood_content,support_count,comment_count,forward_count) values('"+currentQQ+"','"+date+"','"+mood+"',"+support+","+comment+","+foward+");"
            self.connect.insert(sql)
        
        
            
    
    def parseUserInfo(self):
        '''解析用户信息并保存数据库'''
        pass
    
    