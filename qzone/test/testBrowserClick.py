#coding:utf8
'''
Created on 2016-6-21

@author: 浮生若梦
'''

import spynner
from ghost import Ghost


# br = spynner.Browser()
# br.show()
# br.load("http://juicystudio.com/experiments/ajax/index.php")
# br.click("#fact")
# br.wait(10)

ghost = Ghost()
# ghost = ghost.Ghost()
page,ewsources = ghost.open("http://qzone.qq.com")
print page
