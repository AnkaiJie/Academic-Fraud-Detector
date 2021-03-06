'''
Created on Jan 05, 2016

@author: Ankai
'''
from bs4 import BeautifulSoup
import lxml
import re
import time
from ReferenceParser import IeeeReferenceParser, SpringerReferenceParser, PaperReferenceExtractor, PdfObj
import SessionInitializer
import WatLibSeleniumParser


class Paper:
    def __init__ (self, link, loadPdf=True):
        self.__url = link
        self.__pdfObj = None
        self.__pap_info = {}
        self.__pap_info['Publisher'] = ''
        self.__citedByUrl = None
        self.__citedByNum = 0
        self.__allAuthors = None

        #Internet Session Setup
        self.session = SessionInitializer.getSesh()
        self.headers = SessionInitializer.getHeaders()

        self.loadFromGoogleScholar(loadPdf=loadPdf)
        

    def loadFromGoogleScholar(self, loadPdf=True):
        response = self.session.get(self.__url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')
        #print(soup)


        try:
            t = soup.find('a', attrs={'class': 'gsc_title_link'}).text
            self.__pap_info['Title'] = re.sub('(\[.*\])', '', t)
        except AttributeError:
            print(self.__url + 'has no title')
            self.__pap_info['Title'] = "Unknown Title"


        div_info_table = soup.find('div', attrs={'id': 'gsc_table'})
        div_fields = div_info_table.find_all('div', attrs={'class': 'gs_scl'})

        for field in div_fields:
            fieldName = field.find('div', attrs={'class': 'gsc_field'}).text
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

            self.__pap_info[fieldName] = field.find('div', attrs={'class': 'gsc_value'}).text

        if loadPdf:
            self.setPdfObj()

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

    def getInfo(self):
        return self.__pap_info

    def getPdfObj(self):
        return self.__pdfObj

    # Set the PDF object later on if you chose to not load it in the beginning, only works
    # if the pdf object is not already loaded
    def setPdfObj(self):
        if self.__pdfObj is None:
            self.__pdfObj = self.findPdfObjFromUrlOnPage()
            if self.__pdfObj is not None:
                self.__pdfObj.setTitle(self.__pap_info['Title'])

    def findPdfObjFromUrlOnPage(self):
        extractor = GscPdfExtractor()
        return extractor.findPdfFromInfo(self.__url)


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
            return_author = gsc_bot.get_author_from_search(author, paperName)
            if return_author is not -1:
                authorList.append(gsc_bot.get_author_from_search(author, paperName))

        # list of all authors of the paper (if they exist on google scholar) 
        # if they don't exist, they are stored as a string saying they don't exist
        return authorList


    #returns a list of citation objects for this paper
    def findAllCitations(self):
        ref_processor = PaperReferenceExtractor()

        ref_content = ref_processor.getReferencesContent(self.__pdfObj)

        if (self.getInfo()['Publisher'] == 'Springer US'):
            parser = SpringerReferenceParser()
        elif (self.getInfo()['Publisher'] == 'IEEE'):
            parser = IeeeReferenceParser()
        else:
            raise Exception('Publisher not recognized; no citation parser for this format')

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

    def __init__(self, mainUrl, numPapers, loadPaperPDFs=True, pubFilter=False):

        self.first_name = None
        self.last_name = None
        self.url = None
        self.__paper_list = []

        #Internet Session Setup
        self.session = SessionInitializer.getSesh()
        self.headers = SessionInitializer.getHeaders()

        if (mainUrl is not None):
            self.url = mainUrl
            self.loadPapers(numPapers, loadPaperPDFs=loadPaperPDFs, pubFilter=pubFilter)


    def loadPapers(self, numPapers, loadPaperPDFs=True, pubFilter=False, delay=False):
        response = self.session.get(self.url + '&cstart=0&pagesize=' + str(numPapers), headers=self.headers)
        soup = BeautifulSoup(response.content, "lxml")

        full_name = soup.find('div', attrs={'id': 'gsc_prf_in'}).text.lower().split()

        #stores the lowercase first and last names
        self.first_name = full_name[0]
        self.last_name = full_name[1]
        #print(self.last_name)

        print('In loadPapers function for ' + self.first_name + ' ' + self.last_name + '. Num papers: ' + str(numPapers))    

        self.__paper_list = []

        #appends all papers to paperlist
        all_papers = soup.findAll('a', attrs={'class': 'gsc_a_at'}, href=True)
        for one_url in all_papers:
            #one_url['href'] finds the link to the paper page
            p = Paper(SessionInitializer.ROOT_URL + one_url['href'], loadPaperPDFs)
            self.__paper_list.append(p)
            if delay:
                time.sleep(10)
        # takes out all papers not from IEEE or Springer US 
        if pubFilter: 
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

    def __init__(self):
        #Internet Session Setup
        self.session = SessionInitializer.getSesh()
        self.headers = SessionInitializer.getHeaders()

    #returns the list of pdf objects from the first page of citations on Google Scholar
    def findPapersFromCitations(self, citationsUrl):
        response = self.session.get(citationsUrl, headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')

        linkExtracts = soup.findAll('div', attrs={'class': 'gs_r'})
        pdfList = []

        if linkExtracts is None:
            return pdfList


        for extract in linkExtracts:
            title = extract.find('h3', attrs={'class': 'gs_rt'}).text
            if title is not None:
                title = re.sub('(\[.*\])', '', title)
            extract = extract.find('div', attrs={'class': 'gs_ggsm'})
            pdf_obj = PdfObj('local')
            pdf_obj.setTitle(title)
            print(pdf_obj.getTitle())

            if extract is None:
                print('Found PDF title but no PDF link. Returning only title: ' + str(pdf_obj.getTitle()))
                pdfList.append(pdf_obj)
                continue

            #this code will skip links with [HTML] tag and throw error for links that are only "Get it at UWaterloo"
            tag = extract.find('span', attrs={'class': 'gs_ctg2'})
            if tag is not None and tag.text == "[PDF]" and not self.badSource(extract.find('a')):
                pdf_obj.resetContent('url', extract.find('a')['href'])
                print('pdf url: ' + pdf_obj.getPathUrl() + ' has title ' + str(pdf_obj.getTitle()))
                pdfList.append(pdf_obj)
                continue
            elif tag is not None:
                print('Non-PDF tag, using get it @ waterloo')

            potential_links = extract.findAll('a')

            notFound = True
            for link in potential_links:
                if link.text.strip() == "Get It!@Waterloo":
                    print('Get It!@Waterloo')
                    url = SessionInitializer.ROOT_URL + link['href']
                    pdf_obj = self.getWatPDF(url)
                    if pdf_obj is not None:
                        pdf_obj.setTitle(title)
                        notFound = False
                    else:
                        pdf_obj = PdfObj('local')
                        pdf_obj.setTitle(title)
                    break                    

            if notFound:
                print('Found PDF title but no PDF content. Returning only title.' + str(pdf_obj.getTitle()))
            pdfList.append(pdf_obj)



        pdfList = [p for p in pdfList if p is not None]
        return pdfList


    #getting PDF ubject from url on paper info page, different from citation list page
    def findPdfFromInfo(self, infoPageUrl):
        response = self.session.get(infoPageUrl, headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')

        extract = soup.find('div', attrs={'id': 'gsc_title_gg'})
        if extract is None:
            return None

        #find pdf url
        tag = extract.find('span', attrs={'class': 'gsc_title_ggt'})
        if tag is not None and tag.text == "[PDF]" and not self.badSource(extract.find('a')):
            return PdfObj('url', extract.find('a')['href'])
        elif tag is not None:
            print('Non-PDF tag or bad source, using get it @ waterloo')

        potential_links = extract.findAll('div', attrs={'class': 'gsc_title_ggi'})
        for div in potential_links:
            text =  div.text.strip()
            if text == 'Get It!@Waterloo':
                pdf_obj = self.getWatPDF(div.find('a')['href'])
                if pdf_obj is not None:
                    return pdf_obj
        return None

    def badSource(self, html_el):
        bad_sources = ['researchgate']
        if html_el is None:
            return True
        for bs in bad_sources:
            if bs in html_el.text:
                return True
        return False

    # Parses page waterloo gives us to extract pdf of paper
    def getWatPDF(self, url, title=None):
        print(url)
        time.sleep(15)
        status = WatLibSeleniumParser.downloadFromWatLib(url, 'paper.pdf')
        if status is None:
            return None
        else:
            newPdf = PdfObj('local', 'paper.pdf')
            return newPdf



class GscHtmlFunctions:

    def __init__(self):
        #Internet Session Setup
        self.session = SessionInitializer.getSesh()
        self.headers = SessionInitializer.getHeaders()


    def get_author_from_search(self, auth_name, paper_name):
        # taking out any special characters in paper name
        try:
            paper_name = re.sub(r'\W+', ' ', paper_name)
            paper_name = "+".join(paper_name.split())

            authorFields = auth_name.split()
            lastName = authorFields[len(authorFields) - 1]

            #must get query into the right form as noted by GS link first+middle+last
            query = "+".join(authorFields) + "+" + paper_name
        except Exception as e:
            print('Name error when finding author: ' + str(e))
            return None

        response = self.session.get(SessionInitializer.ROOT_URL + '/scholar?q=' + query + '&btnG=&hl=en&as_sdt=0%2C5',
                                    headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')

        try:
            authorsData = soup.find('div', attrs={'class': 'gs_a'}).findAll('a')
            #print (authorsData)
        except Exception as e:
            print('Search function not returning a possibility ' + str(e))
            return None

        for anAuthor in authorsData:
            if (anAuthor.text.find(lastName) != -1):
                link = anAuthor['href']
                #default number of paper loads and corresponding paper objects stored for author is set to 1
                thisAuthor = AcademicPublisher(SessionInitializer.ROOT_URL + link, 1, pubFilter=True)
                return thisAuthor

        print("cannot find author " + auth_name)
        return None

# g = GscPdfExtractor()
# p = g.findPapersFromCitations('https://scholar-google-ca.proxy.lib.uwaterloo.ca/scholar?start=0&hl=en&as_sdt=0,5&sciodt=0,5&cites=10848974562744400393')
# print('-----------------------------------------------')
# for paper in p:
#     analyzer = PaperReferenceExtractor()
#     content = analyzer.getReferencesContent(paper)
#     if content is None and paper.getTitle() is not None:
#         print(paper.getTitle())        
#         print('here2')
#     else:
#         print(paper.getTitle())

#p = Paper('https://scholar-google-ca.proxy.lib.uwaterloo.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&cstart=40&citation_for_view=_yWPQWoAAAAJ:u-coK7KVo8oC')

# pdfExtractor = GscPdfExtractor()
# url='https://scholar-google-ca.proxy.lib.uwaterloo.ca/scholar?start=0&hl=en&as_sdt=0,5&sciodt=0,5&cites=526958332256542107'
# pdfs = pdfExtractor.findPapersFromCitations(url)
# analyzer = PaperReferenceExtractor()


# p = Paper('https://scholar-google-ca.proxy.lib.uwaterloo.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:R3hNpaxXUhUC')
# pre = PaperReferenceExtractor()
# print(pre.getReferencesContent(p.getPdfObj()))

# g = GscPdfExtractor()
# g.findPapersFromCitations('https://scholar.google.ca/scholar?start=20&hl=en&as_sdt=0,5&sciodt=0,5&cites=16000911563998617100')