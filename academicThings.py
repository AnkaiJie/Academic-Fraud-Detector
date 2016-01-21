'''
Created on Jan 05, 2016

@author: Ankai
'''
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from urllib.request import Request, urlopen
import requests
import lxml
import PyPDF2
from _io import BytesIO, BufferedWriter


class Paper:
    def __init__ (self, link):
        self.__url = link
        self.__pap_info = {}
        self.__citersUrl = "none"
        
        session = requests.session()
        response = session.get(self.__url)
        soup = BeautifulSoup(response.content, 'lxml')

        self.__pap_info['Title'] = soup.find('a', attrs={'class': 'gsc_title_link'}).text
        
        div_info_table = soup.find('div', attrs={'id':'gsc_table'})
        div_fields = div_info_table.find_all('div', attrs={'class':'gs_scl'})
        
        for field in div_fields:
            fieldName = field.find('div', attrs={'class':'gsc_field'}).text
            if (fieldName == "Description"):
                continue
            if (fieldName == "Total citations"):
                citedBy = field.find('div', attrs={'style':'margin-bottom:1em'}).find('a')
                self.__pap_info['Citations'] = citedBy.text.replace("Cited by ", "")
                self.__citersUrl = citedBy['href']
                break

            self.__pap_info[fieldName] = field.find('div', attrs={'class':'gsc_value'}).text
        
    def getUrl(self):
        return self.__url
    
    def getCitersUrl(self):
        return self.__citersUrl 
        
    def getInfo (self):
        return self.__pap_info
        
        
class AcademicPublisher:

    def __init__ (self, name, mainUrl):
        
        self.name = name
        self.url = mainUrl        
        self.__paper_list = []
        '''self.url = self.url + '&cstart=0&pagesize=' + str(numResults)
        values = {'s':'basics',
                  'submit':'search'}
        data = urllib.parse.urlencode(values)
        self.data = data.encode(encoding='utf-8')
        req = urllib.request.Request(self.url, self.data)
        resp = urllib.request.urlopen(req)
        self.respData = resp.read()
        #print(self.respData)
        print(self.getWorksListOnPage(self.respData))'''
    
    def getPapers(self, numResults):
        session = requests.Session()
        response = session.get(self.url + '&cstart=0&pagesize=' + str(numResults))
        
        soup = BeautifulSoup(response.content, "lxml")
        print(soup)
        
        for one_url in soup.findAll('a', attrs={'class':'gsc_a_at'}, href=True):
            self.__paper_list.append(Paper('https://scholar.google.ca' + one_url['href']))
    
        return self.__paper_list
    
    def getPaperCitationsByIndex(self, index):
        return self.__paper_list[index].getCitersUrl()
    
class GscPdfExtractor:
    
    def __init__ (self, url):
        self.url = url
        self.__pdfUrls = []
    
    def findPaperUrls(self):
        session = requests.session()
        response = session.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        linkExtracts = soup.findAll('div', attrs={'class':'gs_md_wp gs_ttss'})
        
        for extract in linkExtracts:
            #this code will skip links with [HTML] tag and throw error for links that are only "Get it at UWaterloo"
            try:
                if extract.find('span', attrs={'class':'gs_ctg2'}).text == "[PDF]":
                    self.__pdfUrls.append(extract.find('a')['href'])
                else:
                    print(extract.find('span', attrs={'class':'gs_ctg2'}).text+" tag process will be coded later")
            except:
                print('No tag, "Get it at waterloo" part.. to be coded later')
            
        return self.__pdfUrls
        
class PaperReferenceProcessor:
    
    #assuming type is PDF
    def __init__ (self):
        self.references = []
        
    def getPdfContent (self, pdfUrl):
        
        content =""
        remoteFile = urlopen(Request(pdfUrl)).read()
        localFile = BytesIO(remoteFile)

        pdf = PyPDF2.PdfFileReader(localFile)
        
        for pageNum in range(pdf.getNumPages()):
            content+= pdf.getPage(pageNum).extractText()
            
        content = content.replace(u"/xao", " ")
        return content
    
    def getCitesToAuthor (self, author, pdfContent):
        
        index = pdfContent.find("References")
        if (index==-1):
            index = pdfContent.find("REFERENCES")
        if (index==-1):
            index = pdfContent.find("R\nEFERENCES")
        if (index==-1):
            print("can't find reference sections")
            return -1
        
        refContent = pdfContent[index:]
        
        counter = 0
        while (refContent.find(author)!=-1):
            refIndex = refContent.find(author)
            counter+=1
            refContent = refContent[refIndex+len(author):]
        
        print (counter)
        return counter
    
p = PaperReferenceProcessor()
p.getCitesToAuthor("Gonzalez", p.getPdfContent('http://arxiv.org/pdf/1102.4106.pdf'))
        


    
        
