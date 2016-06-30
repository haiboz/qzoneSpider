#coding:utf8
'''
Created on 2016-6-12

@author: 浮生若梦
'''
import login
import time
import sqlConnect
from qzone.spiderUtils import qqParser

class QQMain(object):
    def __init__(self):
        self.login = login.QZoneLogin()
        self.sqlConnect = sqlConnect.SQLConnect()
        self.qqParser = qqParser.QQParser()
        
        
    def nextuser(self):
        '''获取下一个需要爬取的空间账号,并把该账号置为已爬取'''
        conn = self.sqlConnect.connect()
        cursor = conn.cursor()
        sqlSel = "select id,friend_qq from friend where status = 0 LIMIT 1"
        
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        if rs is not None:
            print rs
            #把该账号置为已爬去
            try:
                sqlUpd = "update friend SET status = 1 where id = %d" % rs[0]
                cursor.execute(sqlUpd)
                conn.commit()#事务提交
                print "已重置"
            except Exception as e:
                print e
                conn.rollback() #事务回滚
            return rs
        else:
            #爬虫结束
            return None
    
    def crawMood(self,browser,currentQQ):
        '''爬取说说信息'''
        browser.get("http://user.qzone.qq.com/%d/311" % currentQQ)#说说
        url = browser.current_url
        print "url = "+url
        time.sleep(0.5)
        browser.switch_to_frame("app_canvas_frame")#定位到iframe  且只能定位一次  再次定位将失效
        source = browser.page_source  #获取加载好的网页信息 提取有效信息
        open("page_shuoshuo.html","w+").write(source)
        self.qqParser.parseMood(currentQQ)
        pass
    
    def crawUserInfo(self,browser,currentQQ):
        '''爬取用户基本信息'''
        pass
    
    def craw(self,count):
        rs = qqMain.nextuser()
        if rs is None:
            print "爬虫结束"
            return count
        else:
            #爬虫继续
            currentNum = rs[0]
            currentQQ = rs[1]
            browser.get("http://user.qzone.qq.com/%d/main" % currentQQ) #进入主页
            #判断能否进入空间
            try:
                mainTag = browser.find_element_by_id("tb_index_ownerfeeds")
            except:
                mainTag = None
            while mainTag is None:#空间为开通或没有访问权限
                rs = qqMain.nextuser()
                currentNum = rs[0]
                currentQQ = rs[1]
                browser.get("http://user.qzone.qq.com/%d/main" % currentQQ) #进入主页
                try:
                    mainTag = browser.find_element_by_id("tb_index_ownerfeeds")
                except:
                    mainTag = None
            print "当前可访问qq:%d" % currentQQ
            #1.爬取用户说说及好友信息
            self.crawMood(browser,currentQQ)
            #2.爬取用户基本信息
            self.crawUserInfo(browser, currentQQ)
            count = count + 1
        return count

if __name__ == "__main__":
    print "进入主函数"
    qqMain = QQMain()
    browser = qqMain.login.loginQQ()#登录qq
    count = 0
    while count < 100:
        count = qqMain.craw(count)
    
        
        
    
    
    if 1 == 2:
        time.sleep(1)
        
        browser.get("http://user.qzone.qq.com/1069757861/1")#个人档
        time.sleep(1)
        url = browser.current_url
        print "url = "+url
        browser.switch_to_frame("app_canvas_frame")#定位到iframe  且只能定位一次  再次定位将失效
        
        source = browser.page_source  #获取加载好的网页信息 提取有效信息
        open("page.html","w+").write(source)
    elif 1==3:
        browser.get("http://user.qzone.qq.com/1069757861/311")#说说列表
        time.sleep(1)
        url = browser.current_url
        print "url = "+url
        browser.switch_to_frame("app_canvas_frame")#定位到iframe  且只能定位一次  再次定位将失效
        
        source = browser.page_source  #获取加载好的网页信息 提取有效信息
        open("page_shuoshuo.html","w+").write(source)
        #<ol id="msgList"   说说内容
    else:
        pass
    
    
    
    










