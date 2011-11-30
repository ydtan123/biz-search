'''
Created on Oct 8, 2011

@author: zul110
'''
from BeautifulSoup import BeautifulSoup as bs
import urlparse
import urllib
import urllib2
from pyquery import PyQuery
import os
import sys
import csv
import simplejson
import tldextract
import re
from sets import Set
import time

'''
example, search hotels in las vegas
http://local.yahooapis.com/LocalSearchService/V3/localSearch?appid=sMt1JZnV34HE3C_KQlyei8jACZ1tuwc8FRmkd1J6UOvdZ_YYphONh6hwU_LhvrX3_GE-&query=hotel&location=lasvegas&results=20
refer to http://developer.yahoo.com/search/local/V3/localSearch.html
'''

YahooAppid = 'sMt1JZnV34HE3C_KQlyei8jACZ1tuwc8FRmkd1J6UOvdZ_YYphONh6hwU_LhvrX3_GE-'
OUTPUT = 'json'
MAXROUND = 250
MAXREQSIZE = 250

OUTPUTEND = 'INFO.csv'


class HotelProcessor:
    def __init__(self):
        fileName = OUTPUTEND
        f = open(fileName, 'wb') 
        self.cvsWriter = csv.writer(f, delimiter='\t')
        
        
    def showHotelList(self, location, searchfor='hotel', requestedSize=20):
        searchfor = searchfor.strip()
        
        startPos = 0
        round = 1
        while 1:
            query = urllib.urlencode({'appid': YahooAppid, 
                                      'query': searchfor, 
                                      'results': requestedSize, 
                                      'location':location, 
                                      'start': startPos,
                                      'output':OUTPUT})
            url = 'http://local.yahooapis.com/LocalSearchService/V3/localSearch?%s' % query
            search_response = urllib.urlopen(url)
            search_results = search_response.read()
            results = simplejson.loads(search_results)
            resList = results['ResultSet']['Result']
                
            for item in resList:
                try:
                
                    burl = item['BusinessUrl']
                    title = item['Title']
                    phone = item['Phone']
                    
                    #domain information
                    ext = tldextract.extract(burl)
                    domaintld = ext.domain + '.' + ext.tld
                    
                    #store and search email
                    emailList = self.searchEmail(domaintld, domaintld)
                    self.storeInformation([title, burl, phone, str(emailList)])
                except:
                    continue
                
            
            startPos += requestedSize
            round += 1
            
            if round >= 250:
                break 
            if len(resList) < 20:
                break ;
            
            
    def storeInformation(self, l):
        self.cvsWriter.writerow(l)
    
    
    #emails = re.findall('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', page)
    def searchEmail(self, businessURL, tld):    
    #    url = ('https://ajax.googleapis.com/ajax/services/search/web'
    #           '?v=1.0&q=contact%20email+site:www.mgmgrand.com&rsz=1')
        ptnStr = '[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z.]*' + tld   
        siteStr = '+site:%s' % businessURL
        searchfor = 'q=contact%20email' + siteStr + '&rsz=5'
        
        url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % searchfor    
        request = urllib2.Request(url, None)
        response = urllib2.urlopen(request)
        
        # Process the JSON string.
        results = simplejson.load(response)
        recList = results['responseData']['results']
        
        emailList = []
        errorURLs = []
        for item in recList:
            try:
                theURL = item['url']
                f = urllib.urlopen(theURL)
                htmlStr = f.read()  
                temp = re.findall(ptnStr, htmlStr) 
                if len(temp) > 0:     
                    emailList += temp
            except:
                errorURLs.append(theURL)
                continue
        
        #try the error rec again.
        for errorURL in errorURLs:
            try:
                f = urllib.urlopen(errorURL)
                htmlStr = f.read()  
                temp = re.findall(ptnStr, htmlStr) 
                if len(temp) > 0:     
                    emailList += temp
            except:
                continue
            
        return list(Set(emailList))

        
HP = HotelProcessor()   
HP.showHotelList('las vegas')    
    
#searchEmail('www.mgmgrand.com', 'mgmgrand.com')

