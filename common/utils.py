import tldextract

EMAILRE = '[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z.]*'

def domain_from_url(cls, url):
    ext = tldextract.extract(url)
    return ext.domain + '.' + ext.tld

class InputManager(object):

    @classmethod
    def obtainURLs(cls):
        """
        obtain unscanned URLs from business table.
        """
        urlList = ["http://www.ac-baidu.com"]
        domainList = ["ac-baidu.com"]
        return urlList, domainList

    @classmethod
    def obtainURLsFromFiles(fileList):
        """
        obtain unscanned URLs from business table.
        """
        urlList = []
        domainList = []
        for fileName in fileList:
            f = open(fileName, 'rb')
            csvReader = csv.reader(f, delimiter = '\t')
            for row in csvReader:
                if row[1]:
                    urlList.append(row[1])
                    domainList.append(domain_from_url(row[1]))

        domainList = list(set(domainList))
        return urlList, domainList

        urlList = 'http://www.yahoo.com'
        domainList = 'yahoo.com'
        return urlList, domainList


    @classmethod
    def obtainURLsFromDB(cls, table=Business):
        """
        obtain unscanned URLs from business table.
        """
        with open_db(dbname='bizsearch') as bizdb:
            dbitems = table.fetch_by(bizdb, ['url', 'country'], "country='US'")
            url_list = [ url for url,_ in dbitems ]
            domain_list = [ domain_from_url(d) for d in url_list ]
        print url_list
        print domain_list
        return url_list, domain_list

    @classmethod
    def obtainURLsFromText(cls, input='url.list'):
        urlList = []
        domainList = []
        with open(input) as furl:
            for line in furl:
                line = line.strip()
                if (line):
                    urlList.append(line)
                    domainList.append(domain_from_url(line))
        domainList = list(set(domainList))
        return urlList, domainList
