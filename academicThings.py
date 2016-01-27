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
    def __init__ (self, link, pdfUrl):
        self.__url = link
        self.__pdfUrl= ""
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
            #don't need the description
            if (fieldName == "Description"):
                continue
            #stores both number of citations and link to citers page as a field
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
    
    def getCitesToAuthor(self, last_name):
        p = PaperReferenceProcessor()
        p.getCitesToAuthor(last_name, p.getPdfContent('http://www.diva-portal.org/smash/get/diva2:517321/FULLTEXT02'))
    
        
class AcademicPublisher:
    
    
    def __init__ (self, mainUrl, numPapers):
        
        self.first_name = None
        self.last_name = None
        self.url = mainUrl        
        self.__paper_list = []
        
        session = requests.Session()
        response = session.get(self.url + '&cstart=0&pagesize=' + str(numPapers))
        soup = BeautifulSoup(response.content, "lxml")
        print(soup)
       
        full_name = soup.find('div', attrs={'id': 'gsc_prf_in'}).text.lower().split()
        print(full_name)
        
        #stores the lowercase first and last names
        self.first_name=full_name[0]
        self.last_name=full_name[1]
        print(self.last_name)
       
       #appends all papers to paperlist
        for one_url in soup.findAll('a', attrs={'class':'gsc_a_at'}, href=True):
            #one_url['href'] finds the link to the paper page
            self.__paper_list.append(Paper('https://scholar.google.ca' + one_url['href']))
       
       
    def getPapers(self, numResults): 
        #returns a list of Papers
        return self.__paper_list
    
    # returners the link to the page with all the citers of a paper with specified index
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
            
        return self.standardize(content)
    
    def getCitesToAuthor (self, author, pdfContent):
        
        index = pdfContent.find("references")
        if (index==-1):
            print("can't find reference sections")
            return -1
        
        refContent = pdfContent[index:]
        
        counter = 0
        while (refContent.find(author)!=-1):
            refIndex = refContent.find(author)
            counter+=1
            refContent = refContent[refIndex+len(author):]
        
        return counter
    
    def standardize(self, str):
        return str.replace("\n", "").replace(" ", "").lower()



#vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 10)
#print(vas.getPaperCitationsByIndex(1))

extractor = GscPdfExtractor('https://scholar.google.ca/scholar?oi=bibs&hl=en&oe=ASCII&cites=2412871699215781213&as_sdt=5')
print(extractor.findPaperUrls())

p = PaperReferenceProcessor()
print(p.getCitesToAuthor('vasilakos', p.getPdfContent('http://www.diva-portal.org/smash/get/diva2:517321/FULLTEXT02')))


    
        
