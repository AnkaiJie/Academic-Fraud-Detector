'''
Created on Jan 05, 2016

@author: Ankai
'''
from bs4 import BeautifulSoup
import requests
import lxml
import re
from ReferenceParser import IeeeReferenceParser, SpringerReferenceParser, PaperReferenceExtractor
import time

class Paper:
    def __init__ (self, link):
        self.__url = link
        self.__pdfUrl= None
        self.__pap_info = {}
        self.__pap_info['Publisher'] = ''
        self.__citedByUrl = None
        self.__citedByNum = 0
        self.__allAuthors = None 
        
        self.loadFromGoogleScholar()
        
    
    def loadFromGoogleScholar(self):
        session = requests.session()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}  
        response = session.get(self.__url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        #print(soup)
       
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
                self.__citedByUrl = citedBy['href']
                self.__citedByNum = int(citedBy.text.replace('Cited by ', '').strip())
                break
            
            self.__pap_info[fieldName] = field.find('div', attrs={'class':'gsc_value'}).text
        
        self.__pdfUrl = self.findPdfUrlOnPage()
    
    def loadFromSpringer(self):
        return
    
    def loadFromIeee(self):
        return
    
    def getUrl(self):
        return self.__url
    
    def getCitedByUrl(self):
        return self.__citedByUrl
    def getCitedByNum(self):
        return self.__citedByNum 
        
    def getInfo (self):
        return self.__pap_info

    def getPdfUrl(self):
        return self.__pdfUrl

    def findPdfUrlOnPage(self):
        extractor = GscPdfExtractor()
        return extractor.findPdfUrlFromInfo(self.__url)
    
    
    # returns a list of author objects - all the authors that collaborated on this paper
    # NOTE: only includes authors that have a google scholar profile!! those that do not are completely omitted
    def findAllAuthors(self):
        authors = self.__pap_info['Authors']
        paperName = self.__pap_info['Title']

        
        authors = authors.split(",")
        #print (authors)
        authorList = []

        gsc_bot = GscHtmlFunctions()
        
        # appends a new authors object as found from the name into the list
        for author in authors:
            return_author  =gsc_bot.get_author_from_search(author, paperName)
            if return_author is not -1:
                authorList.append(gsc_bot.get_author_from_search(author, paperName))
        
        # list of all authors of the paper (if they exist on google scholar) 
        # if they don't exist, they are stored as a string saying they don't exist
        return authorList


   
    #returns a list of citation objects for this paper
    def findAllCitations(self):
        ref_processor = PaperReferenceExtractor()
        
        ref_content = ref_processor.getReferencesContent(self.__pdfUrl)
        
        if (self.getInfo()['Publisher']=='Springer US'):
            parser = SpringerReferenceParser()
        elif (self.getInfo()['Publisher']=='IEEE'):
            parser = IeeeReferenceParser()
        else:
            raise Exception ('Publisher not recognized; no citation parser for this format')
        
        citation_list = parser.citeParse(ref_content)
        
        for idx, citation in enumerate(citation_list):
            citation = Citation(citation)
            citation_list[idx] = citation
        
        return citation_list
        

class Citation:
    #takes dictionary of citation info and makes it into an object
    def __init__(self, info_dict):
        
        self.info_dict = info_dict
        self.authors_list = info_dict['authors']
        self.title = info_dict['title']
        self.year = info_dict['year']
    
    def getInfo(self):
        return self.info_dict
    
    def convertToObjects(self):
        return
        
    
        
class AcademicPublisher:

    def __init__ (self, mainUrl, numPapers):
        
        self.first_name = None
        self.last_name = None
        self.url = None
        self.__paper_list = []
        
        if (mainUrl is not None):
            self.url = mainUrl     
            self.loadPapers(numPapers)
        
       
    def loadPapers(self, numPapers):
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}  
        response = session.get(self.url + '&cstart=0&pagesize=' + str(numPapers), headers=headers)
        soup = BeautifulSoup(response.content, "lxml")

       
        full_name = soup.find('div', attrs={'id': 'gsc_prf_in'}).text.lower().split()
        
        #stores the lowercase first and last names
        self.first_name=full_name[0]
        self.last_name=full_name[1]
        #print(self.last_name)
        
        print('In loadPapers function for ' + self.first_name+' ' + self.last_name +'. Num papers: '+ str(numPapers))    
        
        self.__paper_list=[]
        
        #appends all papers to paperlist
        for one_url in soup.findAll('a', attrs={'class':'gsc_a_at'}, href=True):
            #one_url['href'] finds the link to the paper page
            p = Paper('https://scholar.google.ca' + one_url['href'])
            self.__paper_list.append(p)
            # takes out all papers not from IEEE or Springer US 
            self.filterByPublishers()
        
    def filterByPublishers(self):
        self.__paper_list = [x for x in self.__paper_list if x.getInfo()['Publisher']=='IEEE' or x.getInfo()['Publisher']=='Springer US']
    
    def getPapers(self):
        #returns a list of Papers
        return self.__paper_list
    
    # returns number of times a paper that cited a paper from this author cited the author in total
    # takes the index of the paper in papers list and index of a citer in that paper object
    '''def getNumCitesByPaper(self, indexPaper, indexCiter):
        pdfExtractor = GscPdfExtractor()
        paper = self.__paper_list[indexPaper]
        pdfUrls = pdfExtractor.findPapersFromCitations(paper.getCitedByUrl())

        analyzer = PaperReferenceExtractor()
        content = analyzer.getPdfContent(pdfUrls[indexCiter])
        numCites = analyzer.getCitesToAuthor(self.getLastName(), content)

        return numCites'''

    def getFirstName(self):
        return self.first_name

    def getLastName(self):
        return self.last_name
    
class GscPdfExtractor:
    
    #returns the list of pdf urls from the first page of citations on Google Scholar
    def findPapersFromCitations(self, citationsUrl):
        session = requests.session()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}  
        response = session.get(citationsUrl, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        
        linkExtracts = soup.findAll('div', attrs={'class':'gs_md_wp gs_ttss'})
        pdfUrls = []
        
        for extract in linkExtracts:
            #this code will skip links with [HTML] tag and throw error for links that are only "Get it at UWaterloo"
            try:
                if extract.find('span', attrs={'class':'gs_ctg2'}).text == "[PDF]":
                    pdfUrls.append(extract.find('a')['href'])
                else:
                    print(extract.find('span', attrs={'class':'gs_ctg2'}).text+" tag process will be coded later")
            except:
                print('No tag, "Get it at waterloo" part.. to be coded later')
            
        return pdfUrls

    #getting PDF url from paper info page, different from citation list page
    def findPdfUrlFromInfo(self, infoPageUrl):

        session = requests.session()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}  
        response = session.get(infoPageUrl, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        linkExtracts = soup.findAll('div', attrs={'class':'gsc_title_ggi'})

        for extract in linkExtracts:
            #this code will skip links with [HTML] tag and throw error for links that are only "Get it at UWaterloo"
            try:
                if extract.find('span', attrs={'class':'gsc_title_ggt'}).text == "[PDF]":
                    return extract.find('a')['href']
                else:
                    print("html tag, will figure out later")
                    return None
            except:
                print ("get it at waterloo link, will figure out later")
                return None

class GscHtmlFunctions:
    def get_author_from_search(self, auth_name, paper_name):
        # taking out any special characters in paper name
        paper_name = re.sub(r'\W+', ' ', paper_name)
        paper_name = "+".join(paper_name.split())
        
        authorFields = auth_name.split()
        lastName = authorFields[len(authorFields)-1]
           
        #must get query into the right form as noted by GS link first+middle+last
        query = "+".join(authorFields)+"+"+paper_name

        session = requests.session()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}  
        response = session.get('https://scholar.google.ca/scholar?q='+query+'&btnG=&hl=en&as_sdt=0%2C5', headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        authorsData = soup.find('div', attrs={'class': 'gs_a'}).findAll('a')
        #print (authorsData)
            
        for anAuthor in authorsData:
            if (anAuthor.text.find(lastName) !=-1):
                link = anAuthor['href']
                #default number of paper loads and corresponding paper objects stored for author is set to 1
                thisAuthor = AcademicPublisher('https://scholar.google.ca' + link, 1)
                return thisAuthor

        print("cannot find author "+ auth_name)
        return -1
        


#ozbur = AcademicPublisher('https://scholar.google.ca/citations?user=H1dTZckAAAAJ&hl=en&oi=ao', 8)

'''paper1 = Paper('https://scholar.google.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:u5HHmVD_uO8C')
lst = paper1.findAllAuthors()
for author in lst:
    print(author.getFirstName() + ' ' + author.getLastName())'''
