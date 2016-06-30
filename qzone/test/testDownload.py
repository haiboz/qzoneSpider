#coding:utf8
'''
Created on 2016-6-21

@author: 浮生若梦
'''
import spynner


browser = spynner.Browser()
#加载一个网页
browser.load("http://qzone.qq.com")

print browser.html.encode("utf-8")

open("qqZone.html","w+").write(browser.html.encode("utf-8"))