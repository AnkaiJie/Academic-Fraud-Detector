'''
Created on Jan 05, 2016

@author: Ankai
'''
from bs4 import BeautifulSoup
import requests
import time
from ReferenceParser import IeeeReferenceParser, SpringerReferenceParser, PaperReferenceExtractor, PdfObj

SESSION = requests.Session()

class Paper:
    def __init__ (self, link):
        self.url = link
        self.pdfObj = None
        self.pap_info = {}
        #self.__pap_info['Publisher'] = ''
        self.citedByUrl = None
        self.citedByNum = 0

        #Internet Session Setup
        self.loadFromScopus()

    def loadFromScopus(self):
        response = self.session.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')
        scopux = ScopusPdfExtractor()

        # PDF Object
        ext_link = soup.find('div', attrs={'class': 'sectionCnt'}).find('a', attrs={'class': 'outwardLink'}, href=True)
        ext_link = ext_link['href']
        self.pdfObj = scopux.getWatPDF(ext_link)

        # All Info
        div = soup.find('div', attrs={'id': 'profileleftinside'})
        self.pap_info['journal'] = div.find('sourceCrossMain').find('a').text
        self.pap_info['title'] = div.find('h1', attrs={'class': 'svTitle'}).text
        self.pap_info['author_links'] = []
        for auth_div in div.find('div', attrs={'id': 'authorlist'}).findAll('div'):
            author = auth_div.find('a', attrs={'id': 'Show Author Details'}, href=True)
            if author is not None:
                self.pap_info['author_links'].append(author['href'])

        #Cited by URL
        div_cited = soup.find('div', attrs={'id': 'rightContentSection'}).find('div', attrs={'class': 'docViewAll'})
        href = div_cited.find('a', attrs={'title': 'View all citing documents'}, href=True)
        if href is not None:
            self.citedByUrl = href['href']
        num = div_cited.find('span')
        if num is not None:
            self.citedByNum = int(num.text)

        self.printInfo()

    def printInfo(self):
        print(self.pap_info)
        print(citedByUrl)
        print(citedByNum)

    def getUrl(self):
        return self.url

    def getCitedByUrl(self):
        return self.citedByUrl

    def getCitedByNum(self):
        return self.citedByNum

    def getInfo(self):
        return self.pap_info

    def getPdfObj(self):
        return self.pdfObj


    # returns a list of author objects - all the authors that collaborated on this paper
    # NOTE: only includes authors that have a google scholar profile!! those that do not are completely omitted
    def findAllAuthors(self):
        return

    #returns a list of citation objects for this paper
    def findAllCitations(self):
        return


class AcademicPublisher:

    def __init__(self, mainUrl, numPapers, sortType='relevance'):

        self.first_name = None
        self.last_name = None
        self.paper_list = []
        self.url = mainUrl
        self.rootUrl = mainUrl[:mainUrl.find('.ca') + 3]


        self.loadInfo()
        self.loadPapers(numPapers)
        print(self.first_name + ' ' + self.last_name + ' ' + self.middle_name)

    def loadInfo(self):
        response = SESSION.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')

        title = soup.find('title').text
        title = title[title.find('('):].replace('(','').replace(')', '')
        title = title.split(',')
        self.last_name = title[0].strip().lower()
        firsts = title[1].strip().split(' ')
        self.first_name = firsts[0].strip().lower()
        if (len(firsts) > 1):
            self.middle_name = firsts[1].replace('.','').strip().lower()

        idx = self.url.find('authorId=')
        self.authorId = self.url[idx+9:]


    def loadPapers(self, numPapers, sortType='relevance'):
        if sortType=='relevance':
            sortType = 'cp-f'
        else:
            sortType = 'plf-f'

        url = self.rootUrl + '/author/document/retrieval.uri?authorId=' + self.authorId + '&tabSelected=docLi&sortType=' + sortType + '&resultCount=' + str(numPapers)
        response = requests.get(url)
        
        soup = BeautifulSoup(response.content, 'lxml')
        print(soup)
        pap_list = soup.find('ul', attrs={'id': 'documentListUl'}).findAll('li')
        print(pap_list)
        for paper in pap_list:
            print('here1')
            p = paper.find('span', attrs={'class': "docTitle"})
            p = p.find('a', href=True)
            print(p['href'])
            p = Paper(p['href'])
            self.paper_list.append(p)


    def filterByPublishers(self):
        self.__paper_list = [x for x in self.__paper_list if x.getInfo()['Publisher']=='IEEE' or x.getInfo()['Publisher']=='Springer US']

    def getPapers(self):
        #returns a list of Papers
        return self.__paper_list

    def getFirstName(self):
        return self.first_name

    def getLastName(self):
        return self.last_name


class ScopusPdfExtractor:

    def getWatPDF(self, url, title=None):
        print(url)
        time.sleep(15)
        status = WatLibSeleniumParser.downloadFromWatLib(url, 'paper.pdf')
        if status is None:
            return None
        else:
            newPdf = PdfObj('local', 'paper.pdf')
            return newPdf


a = AcademicPublisher('https://www-scopus-com.proxy.lib.uwaterloo.ca/authid/detail.uri?origin=resultslist&authorId=22954842600', 2)