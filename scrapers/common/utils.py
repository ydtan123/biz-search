import tldextract

EMAILRE = '[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z.]*'

def obtainURLsFromText():
    urlList = []
    domainList = []
    with open('url.list') as furl:
        for line in furl:
            line.strip()
            if (len(line)>0):
                urlList.append(line)
                ext = tldextract.extract(line)
                domaintld = ext.domain + '.' + ext.tld
                domainList.append(domaintld)
    domainList = list(set(domainList))
    return urlList, domainList
