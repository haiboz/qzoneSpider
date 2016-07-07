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
            #把该账号置为已读取
            try:
                sqlUpd = "update friend SET status = 1 where id = %d" % rs[0]
#                 sqlIns = "insert into dealtQq(qq) values(%d)" % rs[0]
#                 cursor.execute(sqlIns)
                cursor.execute(sqlUpd)
                conn.commit()#事务提交
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
    

    
    def insertDealtQQ(self, currentQQ):
        '''把当前qq存入到已被爬取的qq号码表中'''
        sql = "insert into dealtqq(qq) values(%s)" %  currentQQ
        self.sqlConnect.insert(sql)
        
    
    def craw(self,count,maxCount):
        rs = qqMain.nextuser()
        if rs is None:
            print "qq账号已全部爬取"
            return maxCount
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
            while mainTag is None:#空间未开通或没有访问权限
                rs = qqMain.nextuser()
                currentNum = rs[0]#id
                currentQQ = rs[1]#qq
                browser.get("http://user.qzone.qq.com/%d/main" % currentQQ) #进入主页
                try:
                    mainTag = browser.find_element_by_id("tb_index_ownerfeeds")
                except:
                    mainTag = None
            print "第 %d 个可访问qq:%d" % (count,currentQQ)
            #1.爬取用户说说及好友信息
            self.crawMood(browser,currentQQ)
            #1.2 获取说说页面出现的好友qq号码存储
            self.qqParser.parseQQFriend(currentQQ)
            #2.爬取用户基本信息
            self.crawUserInfo(browser, currentQQ)
            #3.把该qq号码存入已被爬取的qq号码表中
            self.insertDealtQQ(currentQQ)
            count = count + 1
        return count

if __name__ == "__main__":
    print "进入主函数"
    qqMain = QQMain()
    qqIndex = 1#使用第几个qq号码登录程序
    browser = qqMain.login.loginQQ(qqIndex)#登录qq
    maxCount = 50#限制爬取的qq最大数
    count = 1#当前已爬去的qq数
    while count < maxCount:
        if count % 5 == 0:
            qqIndex = qqIndex + 1
            browser.close()
            browser = qqMain.login.loginQQ(qqIndex)#登录qq
        try:
            count = qqMain.craw(count,maxCount)
        except:
            open("log_error.log","a+").write("craw error:count = %d" % count)
            print "当前爬取出现异常：%d" % count
    browser.quit()
    print "结束爬虫"
    
        
        
    
    







