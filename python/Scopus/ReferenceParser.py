
'''
Created on Feb 1, 2016

@author: Ankai
'''

import re
from urllib.request import Request, urlopen
import urllib
import PyPDF2
from _io import BytesIO
import WordInference
from math import log

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine



class PdfObj:
    def __init__(self, fileType, pathOrUrl='None'):
        self.pathOrUrl = pathOrUrl
        self.fileType = fileType
        self.localPdfContent = ""
        self.title = None

        if fileType=='local' and pathOrUrl!='None':
            self.storePathPdfContent(pathOrUrl)

    def resetContent(self, fileType, pathOrUrl='None'):
        self.pathOrUrl = pathOrUrl
        self.fileType = fileType
        self.localPdfContent = ""

        if fileType=='local' and pathOrUrl!='None':
            self.storePathPdfContent(pathOrUrl)

    def getFileType(self):
        return self.fileType

    def getPathUrl(self):
        return self.pathOrUrl

    def setTitle(self, t):
        self.title = t

    def getTitle(self):
        return self.title

    def storePathPdfContent(self, path):
        # try:
        #     p = open(self.pathOrUrl, "rb")
        #     pdf = PyPDF2.PdfFileReader(p)
        #     num_pages = pdf.getNumPages()
        #     for i in range(0, num_pages):
        #         self.localPdfContent += pdf.getPage(i).extractText()
        # except PyPDF2.utils.PdfReadError as e:
        #     print('EOF MARKER NOT FOUND' + str(e))
        #     print("LOCAL PATH")
        #     return None
        # except ValueError as e:
        #     print("ValueError " + str(e))
        #     print("LOCAL PATH")
        #     return None
        # except TypeError as e: 
        #     print("TypeError " + str(e))
        #     print("LOCAL PATH")
        #     return None
        # except Exception as e:
        #     print("UNKNOWN EXCEPTION " + str(e))
        #     print("LOCAL PATH")
        #     return None
        k=''
        fp = open(path, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize('')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    k += lt_obj.get_text()
        return k

    def getPdfContent(self):
        content =""
        try:
            if self.fileType == 'url':
                remoteFile = urlopen(Request(self.pathOrUrl)).read()
                localFile = BytesIO(remoteFile)

                pdf = PyPDF2.PdfFileReader(localFile)

                for pageNum in range(pdf.getNumPages()):
                    content+= pdf.getPage(pageNum).extractText()
                return content
            elif self.localPdfContent!="":
                return self.localPdfContent
            else:
                return None
        except urllib.error.URLError as e:
            print('ERROR OPENING PDF WITH URLLIB: '+ str(e))
            print("EXCEPTION PDF URL: " + self.getPathUrl())
            return None
        except PyPDF2.utils.PdfReadError as e:
            print('EOF MARKER NOT FOUND' + str(e))
            print("EXCEPTION PDF URL: " + self.getPathUrl())
            return None
        except ValueError as e:
            print("ValueError " + str(e))
            print("EXCEPTION PDF URL: " + self.getPathUrl())
            return None
        except TypeError as e: 
            print("TypeError " + str(e))
            print("EXCEPTION PDF URL: " + self.getPathUrl())
            return None
        except Exception as e:
            print("UNKNOWN EXCEPTION " + str(e))
            print("EXCEPTION PDF URL: " + self.getPathUrl())
            return None

class PaperReferenceExtractor:
    #assuming type is PDF
    def __init__(self):
        self.references = []

    def filterNoise(self, refContent):
        i = 1
        old_idx = 0
        while(1):
            idx = refContent[old_idx:].find(str(i))
            if idx == -1 or (i > 10 and idx > 400):
                break
            idx += old_idx
            i+=1
            old_idx = idx

        if len(refContent[old_idx:])>200:
            old_idx += 200
        else:
            old_idx += len(refContent[old_idx:])
    
        return refContent[:old_idx]


    def getReferencesContent(self, pdfObj):

        pdfContent = pdfObj.getPdfContent()
        if pdfContent is not None:
            pdfContent = self.standardize(pdfContent)
        else:
            return None
        if pdfContent=="":
            return None
        index = pdfContent.lower().find("references")
        if (index==-1):
            index = pdfContent.lower().find("bibliography")
        if (index==-1):
            print("can't find reference sections")
            return None
        while (index!=-1):
            pdfContent = pdfContent[index +10:]
            index = pdfContent.lower().find("references")

        app_index = pdfContent.lower().find('appendix')
        if (app_index!=-1):
            pdfContent = pdfContent[:app_index]

        abt_authors = pdfContent.lower().find('abouttheauthors')
        if (abt_authors!=-1):
            pdfContent = pdfContent[:abt_authors]

        return self.filterNoise(pdfContent)

    #def parseNoSpaces(self, content):


    # takes in a keyword that symbolizes the author in the PDF, and determines the number of instances of that keyword in the pdf
    def getCitesToAuthor(self, author_key_word, refContent):

        counter = 0
        while (refContent.find(author_key_word) != -1):
            refIndex = refContent.find(author_key_word)
            counter+=1
            refContent = refContent[refIndex+len(author_key_word):]

        return counter

    #removes line breaks, white space, and puts it to lower case
    def standardize(self, thing):
        thing = thing.replace("-\n", "").replace("\n", "").replace(" ","")
        thing = thing.replace("ﬁ", "\"").replace("ﬂ", "\"").replace("™", "\'").replace("œ", "-").replace("Š","-").replace('˚', 'fi')
        return thing


class IeeeReferenceParser:
    # splits whole reference string into individual reference strings
    def splitRefSection(self, section):
        bracket_form = re.compile(r'\[.*?\]')
        section = section.replace('"', '')
        out = [x for x in bracket_form.split(section) if x]

        return out

    # splits a single citation into its components and returns a citation object
    def stringToCitation(self, citation):

        author_and_index = citation.find('and')
        multiple_authors = False
        if (citation[author_and_index+3].isupper() and citation[author_and_index+4]=='.'):
            #this indicates where the last listed author in the reference is 
            citation = citation.replace('and', 'LAST_AUTHOR',1)
            multiple_authors = True

        citation = citation.split(',')
        if(len(citation)<3):
            return None

        authorArray = []
        title = ''
        year = 0

        authors_just_done = False
        title_done = False
        for idx, element in enumerate(citation):
            if (element==""):
                continue
            #for the last author following the and
            if(element.find('LAST_AUTHOR')!=-1):
                element = element.split('LAST_AUTHOR')
                for author in element:
                    if(author!=''):
                        author = ' '.join(author.split('.'))
                        authorArray.append(author)
                authors_just_done = True
            #for all authors before the last one
            elif (element[0].isupper() and element[1]=='.' and authors_just_done is False):
                author = ' '.join(element.split('.'))
                authorArray.append(author)
                if (multiple_authors is False):
                    authors_just_done = True
            #title after authors are finished
            elif(authors_just_done):
                title = element.replace("‚", '').replace('"', '')
                title = WordInference.inferSpaces(title.lower())
                authors_just_done = False
                title_done = True
            #year after title is finished
            elif(title_done):
                i = 1
                for thing in reversed(citation):
                    yr = thing       
                    yr = re.sub('[^0-9]','', yr)
                    try: 
                        year = int(yr)
                    except ValueError:
                        continue
                    if(int(log(year+1, 10)) + 1!=4 or year > 2016):
                        continue
                    break

                break

        print('title: ' + title)
        infoDict = {'authors': authorArray, 'title': title.strip(),
                    'year': year}
        return infoDict

    #wrapper function; given a citation sections, returns array of dictionaries showing data in each citation
    def citeParse(self, ref_section):
        cite_list = self.splitRefSection(ref_section)
        ref_list = []

        for ref in cite_list:
            ref = self.stringToCitation(ref)
            if (ref!=None):
                ref_list.append(ref)

        return ref_list


class SpringerReferenceParser:

    # splits the string into chunks, each one being a citation
    def splitRefSection(self, references):
        i = 2
        ref_list = []
        index = references.find(str(i) + '.')
        while (index != -1):
            temp_ref = references [:index]
            ref_list.append(temp_ref)
            references = references [index:]
            i += 1
            index = references.find(str(i) + '.')

        ref_list.append(references)
        return ref_list

    def stringToCitation(self, ref):

        ref = ref[ref.find('.')+1:]
        ref = re.split('[,.()]', ref)

        author_arr = []
        title = ''
        year = 0

        for idx, element in enumerate(ref):
            if (element.isdigit()):
                year = element
                raw_title = ref[idx + 1].lower()
                raw_title = raw_title.replace('‚', '').replace('"', '')
                #title = re.sub(r'\W+', ' ', raw_title)
                #title = "+".join(title.split())
                title = WordInference.inferSpaces(raw_title)
                break
            else:
                i = -1
                if (element[-4:] == 'etal'):
                    element = element[:-4]

                '''if (element[i:]==element[i:].upper()):
                    author_arr.append(element)
                else:'''
                while (element[i:].isupper()):
                    i -= 1
                    if (i <- 3):
                        break

                element = (element[i + 1:] + ' ' + element[:i + 1])
                author_arr.append(element)

        if (year == 0 or title == ''):
            return None

        infoDict = {'authors': author_arr, 'title': title.strip(),
         'year': year}
        return infoDict

    #given reference section of pdf, returns an array of dictionarys containing author, title, and year info for each reference    
    def citeParse(self, references):
        cite_list = self.splitRefSection(references)
        ref_list = []

        for idx, ref in enumerate(cite_list):
            ref = self.stringToCitation(ref)
            if (ref is not None):
                ref_list.append(ref)

        return ref_list



# extractor = PaperReferenceExtractor()
# # pdf_paper = PdfObj('url', pathOrUrl='http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.636.9687&rep=rep1&type=pdf')
# #pdf_paper = PdfObj('url', pathOrUrl='https://www.researchgate.net/profile/Jun_Luo4/publication/220866049_Compressed_Data_Aggregation_for_Energy_Efficient_Wireless_Sensor_Networks/links/0deec52269881dcd2c000000.pdf')
# pp = PdfObj('url', pathOrUrl='http://novintarjome.com/wp-content/uploads/2014/10/Security-and-privacy-for-storage-and.pdf')
# ref_content = extractor.getReferencesContent(pp)
# print(ref_content)
# print(extractor.getCitesToAuthor('Vasilakos', ref_content))
# #print(ref_content)
# # ieee = IeeeReferenceParser()
# spring = SpringerReferenceParser()
# # print(ieee.citeParse(ref_content))
# print(spring.citeParse(ref_content))