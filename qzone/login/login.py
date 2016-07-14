#coding: utf8
'''
Created on 2016-6-12

@author: 浮生若梦
'''
import os
import time
from selenium import webdriver

class QZoneLogin(object):
    def __init__(self):
        chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        self.browser = webdriver.Chrome(chromedriver,chrome_options=options)
        pass
        
    def getInitInfo(self,index):
        '''获取初始化账号信息'''
        f = open("initUser.txt")
        lines = f.readlines()
        lineNum = 0
        for line in lines:
            if len(line) > 10:
                lineNum = lineNum + 1
        i = 0
        while i <= lineNum:
            if i > 0:
                if index % lineNum == i:
                    #非最后一行
                    s = lines[i-1].split(" ")
                    return s[0],s[1][:-1]#去除换行符
                    pass
            else:
                if index % lineNum == i:
                    #最后一行
                    s = lines[lineNum-1].split(" ")
                    if s[1].find("\n") > 0:
                        return s[0],s[1][:-1]#去除换行符
                    else:
                        return s[0],s[1]
            i = i + 1
        
        
#         if index % lineNum == 1:
#             #第四行
#             line = f.readlines()[0]
#             s = line.split(" ")
#             return s[0],s[1][:-1]#去除换行符
#         elif index % 4 == 3:
#             #第三行
#             line = f.readlines()[2]
#             s = line.split(" ")
#             return s[0],s[1][:-1]#去除换行符
#         elif index % 4 == 2:
#             #第二行
#             line = f.readlines()[1]
#             s = line.split(" ")
#             return s[0],s[1][:-1]#去除换行符
#         elif index % 4 == 1:
#             #第一行
#             line = f.readlines()[0]
#             s = line.split(" ")
#             return s[0],s[1][:-1]#去除换行符
    
    def loginQQ(self,index):
        '''登录qq'''
        #获取初始的账号密码
        user,pwd = self.getInitInfo(index)
        #驱动初始化
        self.__init__()
        #浏览器窗口最大化
        self.browser.maximize_window()
        #浏览器地址定向为qq登陆页面
        self.browser.get("http://qzone.qq.com")
        #定位输入信息frame
        self.browser.switch_to_frame("login_frame")
        #自动点击账号登陆方式
        self.browser.find_element_by_id("switcher_plogin").click()
        #账号输入框输入已知qq账号
        self.browser.find_element_by_id("u").send_keys(user)
        #密码框输入已知密码
        self.browser.find_element_by_id("p").send_keys(pwd)
        #自动点击登陆按钮
        viewFlag = True
        while viewFlag:
            try:
                self.browser.find_element_by_id("login_button").click()
                viewFlag = False
                break
            except:
                viewFlag = True
                time.sleep(0.5)
        time.sleep(1)
        print "登录成功！ 登陆QQ："+user
        return self.browser
    





















