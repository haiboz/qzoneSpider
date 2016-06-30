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
        
    def getInitInfo(self):
        '''获取初始化账号信息'''
        f = open("initUser.txt")
        line = f.readline()
        s = line.split(" ")
        return s[0],s[1]
    
    def loginQQ(self):
        '''登录qq'''
        #获取初始的账号密码
        user,pwd = self.getInitInfo()
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
        time.sleep(1)
        #自动点击登陆按钮
        self.browser.find_element_by_id("login_button").click()
        print "登录成功"
        time.sleep(1)
        return self.browser
    





















