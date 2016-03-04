'''
Created on Feb 1, 2016

@author: Ankai
'''

import re
from urllib.request import Request, urlopen
import PyPDF2
from _io import BytesIO
from WordInference import inferSpaces
import WordInference

class PaperReferenceExtractor:
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
    
    def getReferencesContent(self, pdfUrl):
        
        pdfContent = self.getPdfContent(pdfUrl)
        index = pdfContent.find("References")
        if (index==-1):
            index = pdfContent.find("REFERENCES")
            if (index==-1):
                print("can't find reference sections")
                return -1
        
        while (index!=-1):
            pdfContent = pdfContent[index +10:]
            index = pdfContent.find("References")
            if (index==-1):
                index = pdfContent.find("REFERENCES")
        
        
        return pdfContent
    
    #def parseNoSpaces(self, content):
    
    
    # takes in a keyword that symbolizes the author in the PDF, and determines the number of instances of that keyword in the pdf
    def getCitesToAuthor (self, author_key_word, refContent):

        counter = 0
        while (refContent.find(author_key_word)!=-1):
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
        out = [x for x in bracket_form.split(section) if x]
        
        return out

    # splits a single citation into its components and returns a citation object
    def stringToCitation(self, citation):
        firstSplit = citation.replace("and", " LAST_AUTHOR: ", 1).replace(',', ' ').replace('.', ' ').replace('\"', '')
        firstSplit = firstSplit.split()
        # print(firstSplit)
        
        
        # variables to keep track of where we are in the loop
        finishedAuthors = 0
        finishedTitle = 0
        lastAuthor = 0
        
        # tempVariables to be modified
        tempInitial = ""
        authorArray = []
        year = 0
        title = ""
        
        for idx, el in enumerate(firstSplit):
            # parses the author section
            if (finishedAuthors is 0):
                if (el == "LAST_AUTHOR:"):
                    lastAuthor = 1
                    continue
                elif (len(el) is 1):
                    tempInitial += el + '.'  
                elif (tempInitial == ""):
                    finishedAuthors = 1
                elif (tempInitial != ""):
                    tempInitial += ' '
                    author = tempInitial + el
                    tempInitial = ""
                    authorArray.append(author)
                    if (lastAuthor is 1):
                        finishedAuthors = 1
                        continue
            # gets the year and the title, assuming they come after the author
            if (finishedTitle is 0 and finishedAuthors is 1):
                possibleYr = el.replace('(', '').replace(')', '')
                if (el == 'LAST_AUTHOR:'):
                    continue
                if (possibleYr.isdigit()):
                    # print('in if ' + el)
                    year = int(possibleYr)
                    
                else:
                    # print('in else ' + el)
                    title += inferSpaces(el.lower()) + ' '
                    if (firstSplit[idx + 1] != 'LAST_AUTHOR:'):
                        finishedTitle = 1
        
        # if year was not before the title, it is usually put at the end
        if (year == 0):
            year = firstSplit[-1]
        
        #puts author names to standard format
        for idx, auth in enumerate(authorArray):
            authorArray[idx] = auth.replace('. ', ' ').replace('.', ' ')
            
        infoDict = {'authors': authorArray, 'title': title.strip(), 'year': year}
        return infoDict    
    
    #wrapper function; given a citation sections, returns array of dictionaries showing data in each citation
    def citeParse(self, ref_section):
        cite_list = self.splitRefSection(ref_section)
        ref_list = []
        
        for ref in cite_list:
            ref = self.stringToCitation(ref)
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
                #title = re.sub(r'\W+', ' ', raw_title)
                #title = "+".join(title.split())
                title = WordInference.inferSpaces(raw_title)
                break
            else: 
                i = -1
                if (element[-4:]=='etal'):
                    element = element[:-4]
                
                '''if (element[i:]==element[i:].upper()):
                    author_arr.append(element)
                else:'''
                while (element[i:].isupper()):
                    i -= 1
                    if (i<-3):
                        break
                    
                element = (element[i + 1:] + ' ' + element[:i + 1])
                author_arr.append(element)
            
        infoDict = {'authors': author_arr, 'title': title.strip(), 'year': year}
        return infoDict
        
    #given reference section of pdf, returns an array of dictionarys containing author, title, and year info for each reference    
    def citeParse(self, references):
        ref_list = self.splitRefSection(references)
        cite_list = []
        
        for idx, ref in enumerate(ref_list):
            ref = self.stringToCitation(ref)
            cite_list.append(ref)
        
        return cite_list
            
p = PaperReferenceExtractor()
k = p.getReferencesContent("http://phys.xmu.edu.cn/shuaiweb/ShuaiPub/IEEETN11_135.pdf")
k2 = p.getReferencesContent("http://140.123.102.14:8080/reportSys/file/paper/cktsung/cktsung_39_paper.pdf")
parser = IeeeReferenceParser()
parser2 = SpringerReferenceParser()
print(parser.citeParse(k))
print(parser2.citeParse(k2))


        

