#coding:utf8
'''
Created on 2016-6-21

@author: 浮生若梦
'''
import spynner
import PyQt4

#创建一个浏览器
browser = spynner.Browser()
browser.show()
#浏览器隐藏
# browser.hide()
#加载一个网页

    
# browser.load("http://www.baidu.com")
# # browser.wk_fill('input[id="kw"]', "python1")
# # browser.wk_click('input[id="su"]')
# browser.wk_click('a[id="s_usersetting_top"]',timeout=5)
# 
# browser.wait(10)

# 
browser.load("http://qzone.qq.com")
# browser.wk_fill('input[id="kw"]', "python")
# browser.wk_click('a[href="javascript:void(0);" id="switcher_plogin"]')
print "页面加载"
browser.wait(7)
try:
    print "查找标签"
#     a = browser.webframe.findFirstElement('a#switcher_plogin')
    browser.click("#switcher_plogin")
#     browser.click("a[href='http://im.qq.com/mobileqq/#from=login']")
#     all = browser.webframe.findAllElements('a#switcher_plogin')
#     a = [aa for aa in all if 'Browser' in aa.toPlainText()][0]
    print "点击标签"
#     print a.toPlainText()
#     browser.wk_click_element_link(a, timeout=5)
    print "填入数据"
    browser.wk_fill('input[id="u"]', "106975753")
    browser.wk_fill('input[id="p"]', "223332fsdf")
    print "登录"
    browser.wk_click('input[id="login_button"]')
except Exception as e:
    print e
browser.wait(10)
print "关闭"

# print browser.html.encode("utf-8")

# open("testSpynner.html","w+").write(browser.html.encode("utf-8"))




