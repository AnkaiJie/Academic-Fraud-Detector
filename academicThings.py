'''
Created on Jan 05, 2016

@author: Ankai
'''
from bs4 import BeautifulSoup
import requests
import lxml
import re
from ReferenceParser import IeeeReferenceParser, SpringerReferenceParser, PaperReferenceExtractor

class Paper:
    def __init__ (self, link):
        self.__url = link
        self.__pdfUrl= None
        self.__pap_info = {}
        self.__citedByUrl = None
        self.__allAuthors = None 
        
        self.loadFromGoogleScholar()
        
    
    def loadFromGoogleScholar(self):
        session = requests.session()
        response = session.get(self.__url)
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
        
    def getInfo (self):
        return self.__pap_info

    def getPdfUrl(self):
        return self.__pdfUrl

    def findPdfUrlOnPage(self):
        extractor = GscPdfExtractor()
        return extractor.findPdfUrlFromInfo(self.__url)
    
    
    # returns a list of author objects - all the authors that collaborated on this paper
    def findAllAuthors(self):
        authors = self.pap_info['Authors']
        paperName = self.pap_info['Title']

        # taking out any special characters in paper name
        paperName = re.sub(r'\W+', ' ', paperName)
        paperName = "+".join(paperName.split())
        authors = authors.split(",")
        print (authors)
        authorList = []

        session = requests.session()
        
        # appends a new authors object as found from the name into the list
        for author in authors:
            authorFields = author.split()
            lastName = authorFields[len(authorFields)-1]
            
            #must get query into the right form as noted by GS link first+middle+last
            query = "+".join(authorFields)+"+"+paperName

            
            response = session.get('https://scholar.google.ca/scholar?q='+query+'&btnG=&hl=en&as_sdt=0%2C5')
            soup = BeautifulSoup(response.content, 'lxml')

            authorsData = soup.find('div', attrs={'class': 'gs_a'}).findAll('a')
            #print (authorsData)
            
            foundAuthor = False
            for anAuthor in authorsData:
                if (anAuthor.text.find(lastName) !=-1):
                    link = anAuthor['href']
                    #default number of paper loads and corresponding paper objects stored for author is set to 1
                    thisAuthor = AcademicPublisher('https://scholar.google.ca' + link, 1)
                    authorList.append(thisAuthor)
                    foundAuthor = True
                    break;
                
            if(foundAuthor is False):
                print("cannot find author "+ author)
                authorList.append(lastName+" does not exist in GS database")
        
        # list of all authors of the paper (if they exist on google scholar) 
        # if they don't exist, they are stored as a string saying they don't exist
        return authorList

        '''#returns number of citations this paper makes to the specified author
        def getCitesToAuthor(self, last_name):
        p = PaperReferenceProcessor()
        p.getCitesToAuthor(last_name, p.getPdfContent(self.__pdfUrl))'''
   
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
        self.url = mainUrl        
        self.__paper_list = []
        
        self.loadPapers(mainUrl, numPapers)
        
       
    def loadPapers(self, mainUrl, numPapers):
        session = requests.Session()
        response = session.get(self.url + '&cstart=0&pagesize=' + str(numPapers))
        soup = BeautifulSoup(response.content, "lxml")

       
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
            # takes out all papers not from IEEE or Springer US 
            self.filterByPublishers()
        
    def filterByPublishers(self):
        self.__paper_list = [x for x in self.__paper_list if x.getInfo()['Publisher']=='IEEE' or x.getInfo()['Publisher']=='Springer US']
    
    def getPapers(self):
        #returns a list of Papers
        return self.__paper_list
    
    # returns number of times a paper that cited a paper from this author cited the author in total
    # takes the index of the paper in papers list and index of a citer in that paper object
    def getNumCitesByPaper(self, indexPaper, indexCiter):
        pdfExtractor = GscPdfExtractor()
        paper = self.__paper_list[indexPaper]
        pdfUrls = pdfExtractor.findPapersFromCitations(paper.getCitedByUrl())

        analyzer = PaperReferenceExtractor()
        content = analyzer.getPdfContent(pdfUrls[indexCiter])
        numCites = analyzer.getCitesToAuthor(self.getLastName(), content)

        return numCites

    def getFirstName(self):
        return self.first_name

    def getLastName(self):
        return self.last_name
    
class GscPdfExtractor:
    
    #returns the list of pdf urls from the first page of citations on Google Scholar
    def findPapersFromCitations(self, citationsUrl):
        session = requests.session()
        response = session.get(citationsUrl)
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
        response = session.get(infoPageUrl)
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


        



'''vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1)
for paper in vas.getPapers():
    print (paper.getInfo())'''
'''paper1 = Paper('https://scholar.google.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:u5HHmVD_uO8C')
cite_list = paper1.findAllCitations()

for citation in cite_list:
    print(citation.getInfo())'''


