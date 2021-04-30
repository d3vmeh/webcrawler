from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib import parse
import sys
import math


class pageParser(HTMLParser):
    def handle_starttag(self,tag, attrs):
        if tag == 'a':
            for (key,value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl,value)
                    self.links = self.links+[newUrl]

    def urlLinks(self,url):
        self.links = []
        self.baseUrl = url
        hdr = {'User-Agent':'Mozilla/5.0'}
        req = Request(url, headers=hdr)
        response = urlopen(req)
        if ("text/html") in response.getheader('Content-Type'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

def addLink(currentLinks, newLinks):
    for link in newLinks:
        if (link not in currentLinks) and (rootDomain in link):
            currentLinks.append(link)
    return currentLinks

def open_file(fileName):
    f = open(fileName, mode = 'a')
    return f

def writeData(file,word, url):
    file.write(word+" keyword = "+url+"\n"+"\n")

def crawler(url, keyWords, pageDepth):
    pagesToVisit = [url]
    visitedSoFar = 0
    wordFound = False



    while (visitedSoFar < pageDepth and pagesToVisit != [] and visitedSoFar < len(pagesToVisit )):
        url = pagesToVisit[visitedSoFar]
        visitedSoFar = visitedSoFar +1
        try:
            print(visitedSoFar, "Getting Page: ", url)
            parser = pageParser()
            data, links = parser.urlLinks(url)
            for word in keyWords:
                if data.find(word) >-1:
                    print("------> ",word, "was found on page", url)
                    
                    wordFound = True
                    writeData(data_file,word,url)
            pagesToVisit = addLink(pagesToVisit , links)
        except:
            print("Error!", sys.exc_info()[0],sys.exc_info()[1])

    if (not wordFound):
        print("Word not found")



        
rootDomain = input("Please enter the url of the website ")

k = input("Please enter a keyword ")
k1 = input("Please enter another keyword ")
k2 = input("Please enter one more keyword ")

keyWords = []
keyWords.append(k)
keyWords.append(k1)
keyWords.append(k2)


data_file = open_file("Search_data.txt")
crawler(rootDomain,keyWords,5)   #pageDepth is 50
data_file.close()
print("The data has been successfully been saved to the file")
