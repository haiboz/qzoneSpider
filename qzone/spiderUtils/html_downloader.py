# coding:utf8
'''
Created on 2016年6月25日

@author: 浮生若梦
'''
import urllib2

#下载器
class HtmlDownloader(object):
    
    def download(self,url):
        if url is None:
            return None
        response = urllib2.urlopen(url)
        
        if response.getcode() != 200:
            return None
        cont = response.read()
        return cont.decode("utf8")
    



