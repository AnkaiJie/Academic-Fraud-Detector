'''
Created on Jan 05, 2016

@author: Ankai
'''
from bs4 import BeautifulSoup
import time
from ReferenceParser import IeeeReferenceParser, SpringerReferenceParser, PaperReferenceExtractor, PdfObj
import SessionInitializer
import WatLibSeleniumParser

SESSION = SessionInitializer.getSesh()

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
        response = SESSION.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        scopux = ScopusPdfExtractor()

        # PDF Object
        ext_link = soup.find('div', attrs={'class': 'sectionCnt'}).find('a', attrs={'class': 'outwardLink'}, href=True)
        ext_link = ext_link['href']
        self.pdfObj = scopux.getWatPDF(ext_link)

        # All Info
        div = soup.find('div', attrs={'id': 'profileleftinside'})
        self.pap_info['journal'] = div.find('div', attrs={'class': 'sourceCrossMain'}).find('a').text
        title_div = div.find('h1', attrs={'class': 'svTitle'})
        self.pap_info['title'] = title_div.text.replace('\n', '')
        if title_div.find('span', text=True):
            self.pap_info['title'] = self.pap_info['title'].replace(title_div.find('span', text=True).text, '')

        self.pap_info['author_links'] = []
        for auth_div in div.find('div', attrs={'id': 'authorlist'}).findAll('div'):
            author = auth_div.find('a', attrs={'title': 'Show Author Details'}, href=True)
            if author is not None:
                self.pap_info['author_links'].append(author['href'])

        #Cited by URL
        div_cited = soup.find('div', attrs={'class': 'docViewAll'})
        href = div_cited.find('a', attrs={'title': 'View all citing documents'}, href=True)
        if href is not None:
            self.citedByUrl = href['href']
        num = div_cited.find('span').text
        if num is not None:
            self.citedByNum = int(num)

        self.printInfo()

    def printInfo(self):
        print(self.pap_info)
        print(self.citedByUrl)
        print(self.citedByNum)

    def getUrl(self):
        return self.url

    def getCitedByUrl(self):
        return self.citedByUrl

    def getCitedByNum(self):
        return self.citedByNum

    def getCitingPdfs(self, num):

        cited_by_url = self.getCitedByUrl()
        pdfExtractor = ScopusPdfExtractor()

        offidx = cited_by_url.find('offset=')
        up1 = cited_by_url[:offidx + 7]
        afteridx = cited_by_url[offidx:].find('&')
        up2 = cited_by_url[afteridx + offidx:]
        print(up1)
        print(up2)

        pdfObjs = []

        count = 0
        print('-----------------------------------LOADING CITING PAPERS-----------------------------------')
        for i in range (1, num, 20):
            count += 1
            final_url = up1+str(i)+up2
            print('page url for citations:')
            print(final_url)
            current_pdfObjs = pdfExtractor.findPapersFromCitations(final_url)
            for (p in current_pdfObjs):
                pdfObjs.append(p)
                count += 1
                if count >= num:
                    count = -1
                    break

            if count==-1:
                break

        print('-----------------------------------DONE CITING PAPERS-------------------------------------')
        print('Loaded ' + str(len(pdfObjs)) + ' papers.')

        return pdfObjs


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
        response = SESSION.get(url)
        
        soup = BeautifulSoup(response.content, 'lxml')
        pap_list = soup.find('ul', attrs={'id': 'documentListUl'}).findAll('li')

        for paper in pap_list:
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

    def findPapersFromCitations(url):
        response = SESSION.get(url)
        soup = BeautifulSoup(response.content, 'lxml')

        papers_ul = soup.find('ul', attrs={'class':'documentListUl'})
        paper_divs = papers_ul.findAll('li')

        papers_list = []

        for pdiv in paper_divs:
            title = pdiv.find('span', attrs={'class':'docTitle'}).text
            link = pdiv.find('a', attrs={'titel':'GetIt!@Waterloo(opens in a new window)'}, href=true)
            if link is not None:
                link = link['href']
            new_pdf = self.getWatPDF(link)
            if new_pdf is None:
                new_pdf = PdfObj('local')
            new_pdf.setTitle(title)
            papers_list.append(new_pdf)

        return papers_list





#a = AcademicPublisher('https://www-scopus-com.proxy.lib.uwaterloo.ca/authid/detail.uri?origin=resultslist&authorId=22954842600', 2)