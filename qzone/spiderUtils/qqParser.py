#coding:utf8
'''
Created on 2016-6-24

@author: 浮生若梦
'''
from bs4 import BeautifulSoup
from qzone.login import sqlConnect
import re
import json

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
#             print mood
            #发表日期
            dateTag = li.find("a",attrs={'class':'c_tx c_tx3 goDetail'})
            if dateTag is None:
                date = ""
            else:
                date = dateTag.get_text()
#             print date
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
#             print "赞："+support
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
#             print "评论："+comment
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
#             print "转发："+foward
            index = index + 1
            mood = mood.replace("'", "\\'")#替换说说中出现的单引号',以防止插入失败
            sql = "insert into mood(mood_id,date,mood_content,support_count,comment_count,forward_count) values('%s','%s','%s','%s','%s','%s');" % (currentQQ,date,mood,support,comment,foward)
            self.connect.insert(sql)
        
        
    
    def parseQQFriend(self,currentQQ):
        '''获取说说页面出现的好友qq号码存储'''
        cont = open("page_shuoshuo.html","r+").read()
        soup = BeautifulSoup(cont,"html.parser",from_encoding="utf-8")
        #<a class="nickname" href="http://user.qzone.qq.com/798102408/mood/" target="_self">浮生若梦</a>
        links = soup.find_all("a",attrs = {'class':'nickname','target':'_self'})
        tempQQList = []
        tempNickNameList = []
        for link in links:
            nickName = link.text
            nickName = nickName.replace("'","\\'")
            href = link["href"]
            #截取需要的qq号码
            if len(href) > 10:
                s1 = "com/"
                s2 = "/mood"
                num1 = href.index(s1)
                num2 = href.index(s2)
                qq = href[num1+4:num2]
                tempQQList.append(qq)
                tempNickNameList.append(nickName)
#         tempQQList = list(set(tempQQList))
        qqList = []
        nickNameList = []
        #qq号、昵称去重
        tempQQIndex = 0
        for qq in tempQQList:
            if qq not in qqList:
                qqList.append(qq)
                nickNameList.append(tempNickNameList[tempQQIndex])
            tempQQIndex = tempQQIndex + 1
        tempIndex = 0
        for qq in qqList:
            #如果friend表中未出现过该qq号 则进行存储
            sql = "select friend_qq from friend where friend_qq = %s" % qq
            cursor = self.connect.select(sql)
            if cursor.rowcount == 0:#若没有则插入
                nickName = nickNameList[tempIndex]
#                 nickName = nickName.replace("'","\\'")
                sqlIns = "insert friend(qq_id,friend_qq,friend_nickname,status) values(%s,%s,%s,%d)" % (currentQQ,qq,"'"+nickNameList[tempIndex]+"'",0)
                self.connect.insert(sqlIns)
            tempIndex = tempIndex + 1
#         print qqList         
    
    def parseUserInfo(self,currentQQ):
        '''解析用户信息并保存数据库'''
        userfile = open("page_userinfo.html","r+")
        lines = userfile.readlines()
        userfile.close()
        index = 600
        lineList = lines[index:]
        startIndex = 0
        userStr = ""
        for line in lineList:
            if line.find('g_userProfile') == 0:
                startIndex = index
                break
            index = index + 1
        if startIndex != 0:
            #已获取到个人信息字符串
            userList = lines[startIndex:startIndex+41]
            for s in userList:
                userStr = userStr + s
#             print userStr
            subStart = "{"
            subEnd = "}"
            indexSrart = userStr.find(subStart)
            indexEnd = userStr.find(subEnd)
            userStr = userStr[indexSrart+1:indexEnd]#截取获得最终需要的json数据
            userStr = userStr.replace('"', '')
            userStr = userStr.replace('\n', '')
            userStr = userStr.replace(' ', '')
            ujson = userStr.split(",")
            for element in ujson:
                if element.find("nickname:") == 0:#昵称
                    print "昵称:"+element
                if element.find("spacename:") == 0:#空间名称
                    print "空间名称:"+element
                if element.find("sex:") == 0:#性别
                    print "性别:"+element
                if element.find("age:") == 0:#年龄
                    print "年龄:"+element
                if element.find("birthyear:") == 0:#出生年份
                    print "出生年份:"+element
                if element.find("birthday:") == 0:#出生日期
                    print "出生日期:"+element
                if element.find("bloodtype:") == 0:#血型
                    print "血型:"+element
                if element.find("constellation:") == 0:#星座
                    print "星座:"+element
                if element.find("country:") == 0:#现居地  国家
                    print "现居地  国家:"+element
                if element.find("province:") == 0:#现居地  省份
                    print "现居地  省份:"+element
                if element.find("city:") == 0:#现居地  城市
                    print "现居地  城市:"+element
                if element.find("hco:") == 0:#故乡  国家
                    print "故乡  国家:"+element
                if element.find("hp:") == 0:#故乡  省份
                    print "故乡  省份:"+element
                if element.find("hc:") == 0:#故乡  城市
                    print "故乡  城市:"+element  
                if element.find("marriage:") == 0:#婚姻状况
                    print "婚姻状况:"+element
                if element.find("career:") == 0:#职业
                    print "职业:"+element
                if element.find("company:") == 0:#公司名称
                    print "公司名称:"+element
                if element.find("cco:") == 0:#公司 所在国家
                    print "公司 所在国家:"+element  
                if element.find("cp:") == 0:#公司 所在省份
                    print "公司 所在省份:"+element  
                if element.find("co:") == 0:#公司 所在城市
                    print "公司 所在城市:"+element  
                if element.find("cb:") == 0:#公司 详细地址
                    print "公司 详细地址:"+element  
            print ujson
            
    
    
    