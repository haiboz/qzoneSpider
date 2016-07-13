#coding:utf8
'''
Created on 2016-6-12

@author: 浮生若梦
'''
import login
import time
import sqlConnect
from qzone.spiderUtils import qqParser
from qzone.spiderUtils import commonUtils

class QQMain(object):
    def __init__(self):
        self.login = login.QZoneLogin()
        self.sqlConnect = sqlConnect.SQLConnect()
        self.qqParser = qqParser.QQParser()
        self.commomUtils = commonUtils.CommonUtils()
        
        
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
#         url = browser.current_url
#         print "说说url = "+url
        time.sleep(1)
        try:
            index = 0
            while index < 10:
                try:
                    browser.switch_to_frame("app_canvas_frame")#定位到iframe  且只能定位一次  再次定位将失效
                    break
                except:
                    time.sleep(0.5)
                    print "%d 说说未访问到：%d" % (currentQQ,index)
                index = index + 1
            source = browser.page_source  #获取加载好的网页信息 提取有效信息
            open("page_shuoshuo.html","w+").write(source)
            #解析说说及相关信息
            self.qqParser.parseMood(currentQQ)
        except Exception as e:
            localTime = qqMain.commomUtils.getLocalTime()
            open("log_error.log","a+").write(localTime+" QQ:%d "+"用户说说信息爬取失败:count = %d %s\n" % (currentQQ,count,e))
            print "爬取说说异常！！！"
        pass
    
    def crawUserInfo(self,browser,currentQQ):
        '''爬取用户基本信息'''
        browser.get("http://user.qzone.qq.com/%d" % currentQQ)#个人信息
#         url = browser.current_url
#         print "个人信息url = "+url
        time.sleep(1)
        try:
            index = 0
            while index < 2:
                try:
                    #点击个人档链接
                    browser.find_element_by_xpath("//div[@id='menuContainer']/div/ul/li[6]/a").click()
                    break
                except Exception as e :
#                     print "%d 个人信息未访问到：%d " % (currentQQ,index)
                    time.sleep(0.5)
                index = index + 1
            source = browser.page_source  #获取加载好的网页信息 提取有效的个人信息
            open("page_userinfo.html","w+").write(source)
            #解析用户个人信息
            self.qqParser.parseUserInfo(currentQQ)
        except Exception as e:
            localTime = qqMain.commomUtils.getLocalTime()
            open("log_error.log","a+").write(localTime+" QQ:%d "+"用户个人信息爬取失败:count = %d\n %s" % (currentQQ,count,e))
        pass
        
    
    def insertDealtQQ(self, currentQQ):
        '''把当前qq存入到已被爬取的qq号码表中'''
        sql = "insert into dealtqq(qq) values(%s)" %  currentQQ
        self.sqlConnect.insert(sql)
        
    
    def craw(self,count,maxCount,browser):
        try:
            rs = qqMain.nextuser()
            if rs is None:
                print "qq账号已全部爬取"
                return maxCount
            else:
                #爬虫继续
                #currentNum = rs[0]#id
                currentQQ = rs[1]#qq
                browser.get("http://user.qzone.qq.com/%d/main" % currentQQ) #进入主页
                #判断能否进入空间
                time.sleep(0.5)
                try:
                    mainTag = browser.find_element_by_id("tb_index_ownerfeeds")
                except:
                    mainTag = None
                exceptIndex = 0#判定偶发的登录异常信息
                while mainTag is None:#空间未开通或没有访问权限
                    if exceptIndex == 20:#连续20个空间进入不成功 判定登录异常
                        print "登录发生异常 重新登录！"
                        localTime = self.commomUtils.getLocalTime()
                        open("log_error.log","a+").write(localTime+" "+"login error:登录发生异常 重新登录！\n")
                        browser = qqMain.login.loginQQ(1)#登录qq
                        pass
                    rs = qqMain.nextuser()
                    #currentNum = rs[0]#id
                    currentQQ = rs[1]#qq
                    browser.get("http://user.qzone.qq.com/%d/main" % currentQQ) #进入主页
                    try:
                        mainTag = browser.find_element_by_id("tb_index_ownerfeeds")
                    except:
                        mainTag = None
                        exceptIndex = exceptIndex + 1
                print "第   %d 个可访问qq : %d" % (count,currentQQ)
                #1.爬取用户说说及好友信息
                self.crawMood(browser,currentQQ)
                #1.2 获取说说页面出现的好友qq号码存储
                try:
                    self.qqParser.parseQQFriend(currentQQ)
                except Exception as e:
                    localTime = self.commomUtils.getLocalTime()
                    open("log_error.log","a+").write(localTime+" "+"craw error:count = %d\n" % count)
                    print e
                #2.爬取用户基本信息
                try:
                    self.crawUserInfo(browser, currentQQ)
                except Exception as e:
                    localTime = self.commomUtils.getLocalTime()
                    open("log_error.log","a+").write(localTime+" "+"craw error:count = %d\n" % count)
                #3.把该qq号码存入已被爬取的qq号码表中
                try:
                    self.insertDealtQQ(currentQQ)
                except Exception as e:
                    localTime = self.commomUtils.getLocalTime()
                    open("log_error.log","a+").write(localTime+" "+"craw error:count = %d\n" % count)
                count = count + 1
        except Exception as e:
            localTime = self.commomUtils.getLocalTime()
            open("log_error.log","a+").write(localTime+" "+"craw error:count = %d %s\n" % (count,e))
        return count

    

if __name__ == "__main__":
    print "进入主函数"
    startTime = time.time()
    qqMain = QQMain()
    qqIndex = 1#使用第几个qq号码登录程序
    browser = qqMain.login.loginQQ(qqIndex)#登录qq
    maxCount = 500#限制爬取的qq最大数
    count = 1#当前爬去的qq数
    while count <= maxCount:
#         if count % 100 == 0:
#                 print "程序休眠5秒"
#                 time.sleep(5)
        if count % 10 == 9:
            qqIndex = qqIndex + 1
            browser.quit()
            loginFlag = True
            loginCount = 0
            while loginFlag:
                try:
                    browser = qqMain.login.loginQQ(qqIndex)#登录qq
                    loginFlag = False
                except Exception as e:
                    loginFlag = True
                    localTime = qqMain.commomUtils.getLocalTime()
                    open("log_error.log","a+").write(localTime+" "+"login error:%s \n" % e)
                    loginCount = loginCount + 1
                    if loginCount > 5:
                        break
        try:
            #爬虫主程序
            count = qqMain.craw(count,maxCount,browser)
        except:
            localTime = qqMain.commomUtils.getLocalTime()
            open("log_error.log","a+").write(localTime+" "+"craw error:count = %d\n" % count)
            print "当前爬取出现异常：%d" % count
    browser.quit()
    print "爬虫结束！有效数据  %d 个！" % maxCount
    endTime = time.time()
    seconds = endTime - startTime
    print "共耗时  %d 秒！即  %d 时  %d 分  %d 秒 ！" % (seconds,seconds/3600,(seconds%3600)/60,seconds%60)
    
        
        
    
    







