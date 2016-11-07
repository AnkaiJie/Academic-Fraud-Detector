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
    def __init__ (self, link, loadPaperPDFs=True):
        self.url = link
        self.pdfObj = None
        self.pap_info = {}
        #self.__pap_info['Publisher'] = ''
        self.citedByUrl = None
        self.citedByNum = 0

        #Internet Session Setup
        self.loadFromScopus(loadPaperPDFs=loadPaperPDFs)

    def loadFromScopus(self, loadPaperPDFs=True):
        response = SESSION.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')

        # PDF Object
        if loadPaperPDFs:
            self.setPdfObj()

        # All Info
        div = soup.find('div', attrs={'id': 'profileleftinside'})

        journaldiv = div.find('div', attrs={'class': 'sourceCrossMain'}).find('a')
        if journaldiv is not None:
            self.pap_info['journal'] = journaldiv.text
        else:
            self.pap_info['journal'] = None

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
            resp = SESSION.get(self.citedByUrl, allow_redirects=False)
            self.citedByUrl = resp.headers['Location']
        num = div_cited.find('span').text
        if num is not None:
            self.citedByNum = int(num)

    def printInfo(self):
        print(self.pap_info)
        print(self.citedByUrl)
        print(self.citedByNum)

    def setPdfObj(self):
        response = SESSION.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        scopux = ScopusPdfExtractor()
        ext_link = soup.find('div', attrs={'class': 'sectionCnt'}).find('a', attrs={'class': 'outwardLink'}, href=True)
        ext_link = ext_link['href']
        self.pdfObj = scopux.getWatPDF(ext_link)

    def getUrl(self):
        return self.url

    def getCitedByUrl(self):
        return self.citedByUrl

    def getCitedByNum(self):
        return self.citedByNum

    def getCitingPdfs(self, num):

        cited_by_url = self.getCitedByUrl()
        pdfExtractor = ScopusPdfExtractor()

        offidx = cited_by_url.find('&origin=')
        up1 = cited_by_url[:offidx]
        up2 = cited_by_url[offidx:]
        pdfObjs = []

        count = 0
        inpage = 20
        print('-----------------------------------LOADING CITING PAPERS-----------------------------------')
        for i in range (0, num, inpage):

            final_url = up1 + '&offset=' + str(i+1) + up2
            print('page url for citations:')
            print(final_url)

            toload = 20
            if num-count < inpage:
                toload = num-count

            current_pdfObjs = pdfExtractor.findPapersFromCitations(final_url, toload)
            for p in current_pdfObjs:
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

    def __init__(self, mainUrl, numPapers, sortType='relevance', loadPaperPDFs=False):

        self.first_name = None
        self.last_name = None
        self.paper_list = []
        self.url = mainUrl
        self.rootUrl = mainUrl[:mainUrl.find('.ca') + 3]


        self.loadInfo()
        self.loadPapers(numPapers, loadPaperPDFs=loadPaperPDFs)
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


    def loadPapers(self, numPapers, loadPaperPDFs=True, sortType='relevance'):
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
            p = Paper(p['href'], loadPaperPDFs=loadPaperPDFs)
            self.paper_list.append(p)


    def filterByPublishers(self):
        self.__paper_list = [x for x in self.__paper_list if x.getInfo()['Publisher']=='IEEE' or x.getInfo()['Publisher']=='Springer US']

    def getPapers(self):
        #returns authors papers
        return self.paper_list

    def getFirstName(self):
        return self.first_name

    def getLastName(self):
        return self.last_name


class ScopusPdfExtractor:

    def getWatPDF(self, url, title=None, pdfName='paper.pdf'):
        print('Getting pdf from WatLib')
        print(url)
        status = WatLibSeleniumParser.downloadFromWatLib(url, 'paper.pdf')
        if status is None:
            print('None status')
            return None
        else:
            # try:
            newPdf = PdfObj('local', pdfName)
            # except KeyboardInterrupt:
            #     return None
            return newPdf

    def findPapersFromCitations(self, url, toload):
        response = SESSION.get(url)
        soup = BeautifulSoup(response.content, 'lxml')

        papers_ul = soup.find('ul', attrs={'id':'documentListUl'})
        paper_divs = papers_ul.findAll('li')

        papers_list = []

        count = 0
        for pdiv in paper_divs:
            title = pdiv.find('span', attrs={'class':'docTitle'}).text.replace('\n', '')
            link = pdiv.find('a', attrs={'class':'outwardLink'}, href=True)

            #if there is no valid waterloo link, try to find one
            while link.find('img', attrs={'title':'GetIt!@Waterloo(opens in a new window)'}) is None:
                link = pdiv.find('a', attrs={'class':'outwardLink'}, href=True)
                if link is None:
                    break

            new_pdf = None
            if link is not None:
                link = link['href']
                new_pdf = self.getWatPDF(link)
            
            if new_pdf is None:
                new_pdf = PdfObj('local')

            new_pdf.setTitle(title)
            papers_list.append(new_pdf)

            count += 1
            # only load num specified
            if (count>=toload):
                break

        return papers_list

# sc = ScopusPdfExtractor()
# sc.getWatPDF('https://www-scopus-com.proxy.lib.uwaterloo.ca/redirect/linking.uri?targetURL=http%3a%2f%2fsfx.scholarsportal.info%2fwaterloo%3fsid%3dElsevier%3aScopus%26_service_type%3dgetFullTxt%26issn%3d16871472%26isbn%3d%26volume%3d2016%26issue%3d1%26spage%3d%26epage%3d%26pages%3d%26artnum%3d181%26date%3d2016%26id%3ddoi%3a10.1186%252fs13638-016-0680-7%26title%3dEurasip%2bJournal%2bon%2bWireless%2bCommunications%2band%2bNetworking%26atitle%3dUnderstanding%2bSTDMA%2bvia%2bcomputer%2bsimulation%253a%2bfeasibility%2bto%2bvehicular%2bsafety%2bapplications%252c%2bconfigurations%252c%2band%2btime%2bsynchronization%2berrors%26aufirst%3dJ.-H.%26auinit%3dJ.-H.%26auinit1%3dJ%26aulast%3dLim&locationID=2&categoryID=6&eid=2-s2.0-84981156913&issn=16871472&linkType=TemplateLinking&year=2016&zone=outwardlinks&origin=resultslist&dig=f27235173a5b4809def53afe4c6884f2&recordRank=4\
# ', pdfName='paper.pdf')