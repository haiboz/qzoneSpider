#coding:utf8
'''
Created on 2016-6-21

@author: 浮生若梦
'''
from selenium import webdriver



driver = webdriver.PhantomJS()
driver.get("http://qzone.qq.com")
data = driver.find_element_by_id("switcher_plogin")
print data
driver.quit()