'''
Created on Oct 8, 2011

@author: zul110
'''
import urlparse
import urllib
import csv
import simplejson
import tldextract
import re
from sets import Set
from optparse import OptionParser

'''
example, get local business in a certain location using Yahoo Local API
http://local.yahooapis.com/LocalSearchService/V3/localSearch?appid=sMt1JZnV34HE3C_KQlyei8jACZ1tuwc8FRmkd1J6UOvdZ_YYphONh6hwU_LhvrX3_GE-&query=hotel&location=lasvegas&results=20
refer to http://developer.yahoo.com/search/local/V3/localSearch.html
'''

YahooAppid = 'sMt1JZnV34HE3C_KQlyei8jACZ1tuwc8FRmkd1J6UOvdZ_YYphONh6hwU_LhvrX3_GE-'
OUTPUT = 'json'
MAXROUND = 250
MAXREQSIZE = 250

OUTPUTEND = 'YahooList'
REQSIZE = 20


class YahooGetList:
    """
    Get local businsess list specified by location and type.
    """
    def __init__(self, location, type):
        self.location = location
        self.typeStr = type
        
        loc = location.replace(' ', '')
        loc = loc.replace("'", "")
        type = type.replace("'", "")
                     
        fileName = '_'.join([OUTPUTEND, type, loc])
        self.fileHandler = open(fileName, 'wb') 
        self.cvsWriter = csv.writer(self.fileHandler, delimiter='\t')
        
        
    def showHotelList(self):
        self.typeStr = self.typeStr.strip()
        
        startPos = 0
        round = 1
        while 1:
            try:
                oldStartPos = startPos
                query = urllib.urlencode({'appid': YahooAppid, 
                                          'query': self.typeStr, 
                                          'results': REQSIZE, 
                                          'location':self.location, 
                                          'start': startPos,
                                          'output':OUTPUT})
                url = 'http://local.yahooapis.com/LocalSearchService/V3/localSearch?%s' % query
                search_response = urllib.urlopen(url)
                search_results = search_response.read()
                results = simplejson.loads(search_results)
                resList = results['ResultSet']['Result']
                
                print 'New Round, obtain %d records' % len(resList) 
                for item in resList:
                    try:
                    
                        burl = item['BusinessUrl']
                        title = item['Title']
                        phone = item['Phone']
                        category = self.typeStr
                        loc = self.location
                        status = 'U'
                        owner = 'unknown'
                        
                        #domain information
                        ext = tldextract.extract(burl)
                        domaintld = ext.domain + '.' + ext.tld
                        
                        #store and search email
                        self.storeInformation([title, burl, phone, category, loc, status, owner, domaintld])
                        #print [title, burl, phone, category, loc, status, owner, domaintld]
                    except:
                        continue
                    
                
                startPos += REQSIZE
                round += 1
                
                if startPos >= 250:
                    break 
                if len(resList) < 20:
                    break ;
            except:
                startPos = oldStartPos
                continue
                print 'error:' + str(startPos)
            
    def storeInformation(self, l):
        self.cvsWriter.writerow(l)
    


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--type", dest = "typestr", 
                      help = "business type, e.g., hotel")
    parser.add_option("-l", "--location", dest = "location", 
                      help = "business location, e.g., las vegas")
    
    (options, args) = parser.parse_args()
    print args
    
    if options.typestr and options.location:
        HP = YahooGetList(options.location, options.typestr) 
        HP.showHotelList()
    else:
        print 'Error: no type or location information.'

