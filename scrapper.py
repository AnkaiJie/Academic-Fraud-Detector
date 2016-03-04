'''
Created on Jan 7, 2016

@author: Ankai
'''

from academicThings import AcademicPublisher, GscHtmlFunctions
from academicThings import GscPdfExtractor
from academicThings import Paper
from academicThings import Citation
from ReferenceParser import PaperReferenceExtractor, SpringerReferenceParser,IeeeReferenceParser
from bs4 import BeautifulSoup
import requests
from collections import Counter

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

# given first name, last name, publisher of paper, returns how their name would show in a paper
# published by the given publisher in references section
def get_ref_author_format(fname, lname, pub):
    if (fname == -1 or lname == -1):
        print('Error: author: ' + fname + ' ' + lname + ' is not a valid author of this paper.')
    
    print('reference type: ' + pub)
    
    auth_word = ''
    if (pub =='IEEE'):
        auth_word = ieee_author_keyword_converter(fname, lname)
        return auth_word
    elif (pub =='Springer US'): 
        auth_word = springer_author_keyword_converter(fname, lname)
        return auth_word
    else: 
        print('The given paper is not published from Springer or IEEE. Error.')
        return -1
    

# given a paper, counts the number of times it cites an author of the paper
def count_self_cites(author, paper):
    paper_authors = paper.getInfo()['Authors'].lower()
    fname = author.getFirstName()
    lname = author.getLastName()
    
    '''fname = 'athanasios'
    lname = 'vasilakos'''
    
    
    if (paper_authors.find(fname) == -1 or paper_authors.find(lname) == -1):
        print('Error: author: ' + fname + ' ' + lname + ' is not a valid author of this paper.')
        return -1
    
    auth_word = get_ref_author_format(fname, lname, paper.getInfo()['Publisher'])
    
    analyzer = PaperReferenceExtractor()
    numCites = analyzer.getCitesToAuthor(auth_word, analyzer.getReferencesContent(paper.getPdfUrl()))
    print (fname+ ' '+lname+ ' has '+str(numCites)+' number of self-cites in paper: '+ paper.getInfo()['Title'])
    
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


# given an author, takes x_most_rel number of papers and finds the top_x most cited authors, with total citation count
# then, takes each of those authors, and determines how many times they cite the given author in their x_most_rel number of papers
def count_cross_cites (author, x_most_rel, top_x):
    paper_list = author.loadPapers(x_most_rel)
    print("Total number of valid GSC papers: " + len(paper_list))
    citation_list= []
    
    ref_processor = PaperReferenceExtractor()
    springer_bot = SpringerReferenceParser()
    ieee_bot = IeeeReferenceParser()
    
    # gets all the citations from all the papers in the list
    for paper in paper_list:
        pub = paper.getInfo()['Publisher']
        pdfurl = paper.getPdfUrl()
        ref_content = ref_processor.getReferencesContent(pdfurl)
        
        if (pub=='IEEE'):
            citations = ieee_bot.citeParse(ref_content)
        elif (pub=='Springer US'):
            citations = springer_bot.citeParse(ref_content)
        else:
            print('Invalid publication format from: '+pub)
            return -1
        
        citation_list += citations  
    
    
    author_dist = {}
    
    #goes through each citation and takes out authors and paper names and puts it in the valid frequency dictionary
    # end results: {'author': {'freq': int frequency original author cites him, 'paper': [array of paper titles in which the cited author is cited]}, 
    for citation in citation_list:
        title = citation['title']
        for author in citation['authors']:
            if author in author_dist:
                author_dist[author]['freq'] += 1
                if title not in author_dist[author]['papers']:
                    author_dist[author]['papers'].append(title)
            else:
                author_dist[author]['freq'] = 1
                author_dist[author]['papers'] = [title]
    
    print('unsorted author list: ' + author_dist)
    
    #sorts the dictionary - now an array of tuples that are sorted by frequency
    #author_dist should be in the form [('author', {'freq': 5, 'papers':[]}), ...]
    author_dist = list(reversed(sorted(author_dist.items(), key=lambda x: x[1]['freq'])))
    
    print('sorted author list in tuples: ' + author_dist) 
    
    gsc_bot = GscHtmlFunctions()
    top_x_authors = []
    
    #this part will create valid author objects for each of the top cited authors and append it to a list
    for index, author_info in enumerate (author_dist):
        if (index>top_x-1):
            break
        
        #author info should be in the form ('author', {'freq': 5, 'papers':[]})
        first_paper_title = author_info[1]['papers'][0]
        frequency = author_info[1]['freq']
        author_name = author_info[0]
        returned_author = gsc_bot.get_author_from_search(author_name, first_paper_title)
        if returned_author is -1:
            #if can't find gsc profile for author, go onto the next top cited author
            top_x +=1
        else:
            #each value is an array of two values: author object, and frequency cited
            top_x_authors.append([returned_author, frequency])
            
    print('Top citing authors: ')
    print(top_x_authors)
    
    #gets number of times each of these authors cites the original author
    
    # array to store another array of author, and how many times they cite the original author
    cited_author_info_arr = []
    
    for cited_author in top_x_authors:
        cited_author.loadPapers(x_most_rel)
        temp_paper_lst = cited_author.getPapers()
        total_cites = 0
        
        #determines number of times the paper cites the original author
        for paper in temp_paper_lst:
            analyzer = PaperReferenceExtractor()
            content = analyzer.getReferencesContent(paper.getPdfUrl())
            auth_word = get_ref_author_format(author.getFirstName(), author.getLastName(), paper.getInfo()['Publisher'])
            total_cites += analyzer.getCitesToAuthor(auth_word, content)
            
        cited_author_info_arr.append([cited_author, total_cites])
    
    print('cited_author_info_arr: '+cited_author_info_arr)
    
    #compilation of all the information
    final_info_dict = {'First Name': author.getFirstName(),'Last Name': author.getLastName(), 'Author_citation_frequency': top_x_authors, 'Cited_authors_overcite_frequency':cited_author_info_arr}
    
    return final_info_dict
    
        
    


vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1)
#p = Paper('https://scholar.google.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:u5HHmVD_uO8C')

#print(str(count_overcites_by_index(p, 0, vas)))

count_self_cites(vas, Paper('https://scholar.google.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:2osOgNQ5qMEC'))

'''smeaton = AcademicPublisher('https://scholar.google.ca/citations?user=o7xnW2MAAAAJ&hl=en&oi=ao', 1)
print(smeaton.getFirstName() + ' ' + smeaton.getLastName())'''

#print(count_journal_frequency(vas, 0))








