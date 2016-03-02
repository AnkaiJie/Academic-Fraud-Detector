'''
Created on Jan 7, 2016

@author: Ankai
'''

from academicThings import AcademicPublisher
from academicThings import GscPdfExtractor
from academicThings import Paper
from academicThings import Citation
from ReferenceParser import PaperReferenceExtractor
from bs4 import BeautifulSoup
import requests

#these two functions take and authors first name and last name, and convert them to how it would appear in the references
# section of a paper from the specified publisher
def springer_author_keyword_converter (fname, lname):
    fname_letter = fname[0].upper()
    last_name = lname.title()
    return last_name + fname_letter

def ieee_author_keyword_converter (fname, lname):
    fname_letter = fname[0].upper()
    last_name = lname.title()
    return  fname_letter+'.'+last_name


# given paper and author, and index number, returns number of times a citing paper of index idx 
# also cites the same author
def count_overcites_by_index (paper, idx, author):
    pdfExtractor = GscPdfExtractor()
    pdfUrls = pdfExtractor.findPapersFromCitations(paper.getCitedByUrl())
    # print(pdfUrls)

    analyzer = PaperReferenceExtractor()
    content = analyzer.getReferencesContent(pdfUrls[idx])
    # print(content)
    
    lname = author.getLastName().title()
    
    numCites = analyzer.getCitesToAuthor(lname, content)
    
    print("Citing paper number  " + str(idx+1) + " cites " + lname + " " + str(numCites) + " times.")
    
    return numCites
    

# given a paper, counts the number of times it cites the author of the paper
def count_self_cites(paper, author):
    paper_authors = paper.getInfo()['Authors'].lower()
    fname = author.getFirstName()
    lname = author.getLastName()
    
    '''fname = 'athanasios'
    lname = 'vasilakos'''
    
    
    if (paper_authors.find(fname) == -1 or paper_authors.find(lname) == -1):
        print('Error: author: ' + fname + ' ' + lname + ' is not a valid author of this paper.')
    
    ref_type = paper.getInfo()['Publisher']
    print('reference type: ' +ref_type)
    
    auth_word = ''
    if (ref_type =='IEEE'):
        auth_word = ieee_author_keyword_converter(fname, lname)
    elif (ref_type =='Springer US'): 
        auth_word = springer_author_keyword_converter(fname, lname)
    else: 
        print('The given paper is not published from Springer or IEEE. Error.')
        return -1
    
    analyzer = PaperReferenceExtractor()
    numCites = analyzer.getCitesToAuthor(auth_word, analyzer.getReferencesContent(paper.getPdfUrl()))
    print ('Number of self-cites: '+ str(numCites))
    
    return numCites


#given an author, and an index of one of their papers, returns the journal frequency list of the first ten
# citing papers
def count_journal_frequency (author, index):

    author.loadPapers(index+1);
    cited_by_url = author.getPapers()[index].getCitedByUrl()
    
    
    session = requests.Session()
    response = session.get(cited_by_url)
    soup = BeautifulSoup(response.content, "lxml")
    
    info_list = soup.findAll('div', attrs={'class':'gs_a'})
    
    journal_dict = {}
        
    for info_str in info_list:
        info_str = info_str.text
        info_str = info_str.split('-')[1].split(',')[0]
        #print('final info string: ' + info_str)
        
        if (info_str in journal_dict):
            journal_dict[info_str]+=1
        else:
            journal_dict[info_str] = 1
        
    
    return journal_dict









vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1)
p = Paper('https://scholar.google.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:u5HHmVD_uO8C')

print(str(count_overcites_by_index(p, 0, vas)))

#count_self_cites(Paper('https://scholar.google.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:-95Q15plzcUC'))

'''smeaton = AcademicPublisher('https://scholar.google.ca/citations?user=o7xnW2MAAAAJ&hl=en&oi=ao', 1)
print(smeaton.getFirstName() + ' ' + smeaton.getLastName())'''

#print(count_journal_frequency(vas, 0))








