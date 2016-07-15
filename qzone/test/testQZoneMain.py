#coding:utf8
'''
Created on 2016-6-12

@author: 浮生若梦
'''
import testLogin
import time

class QQmain(object):
    def __init__(self):
        self.login = testLogin.QZoneLogin()

if __name__ == "__main__":
    print "进入主函数"
    qqMain = QQmain()
    user = "5435354"
    pwd = "werewr."
    browser = qqMain.login.loginQQ(user, pwd)
    browser.get("http://user.qzone.qq.com/1069757861/main")
    if 1 == 2:
        time.sleep(1)
        browser.get("http://user.qzone.qq.com/1069757861/1")#个人档
        time.sleep(1)
        url = browser.current_url
        print "url = "+url
        browser.switch_to_frame("app_canvas_frame")#定位到iframe  且只能定位一次  再次定位将失效
        
        source = browser.page_source  #获取加载好的网页信息 提取有效信息
        open("page.html","w+").write(source)
    elif 1==1:
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
    
    
    
    










