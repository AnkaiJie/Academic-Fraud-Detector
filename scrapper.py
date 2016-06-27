'''
Created on Jan 7, 2016

@author: Ankai
'''

from academicThings import AcademicPublisher, GscHtmlFunctions
from academicThings import GscPdfExtractor
from ReferenceParser import PaperReferenceExtractor, SpringerReferenceParser, IeeeReferenceParser
from bs4 import BeautifulSoup
import requests
import time
import PyPDF2
from csvWriter import *


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


# given paper and author, and index number, returns number of times a each
# citing paper on the first page of citing papers also cites the same author
def count_overcites (paper, author):
    time.sleep(10)
    pdfExtractor = GscPdfExtractor()
    pdfObjs = pdfExtractor.findPapersFromCitations(paper.getCitedByUrl())
    # print(pdfUrls)
    analyzer = PaperReferenceExtractor()
    overcites_info = []

    for idx, pdf in enumerate(pdfObjs):
        content = analyzer.getReferencesContent(pdf)

        if (content is None):
            continue

        # print(content)
        lname = author.getLastName().title()
        numCites = analyzer.getCitesToAuthor(lname, content)
        print("Citing paper number  " + str(idx+1) + " cites " + lname + " " + str(numCites) + " times.")
        info_dict = {}
        info_dict['Citing Paper Number'] = idx+1
        info_dict['Over-cite Count'] = numCites
        overcites_info.append(info_dict)

    return overcites_info


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
def count_self_cites(author, num_load):
    author.loadPapers(num_load)
    self_cite_arr = []
    print("Author fully loaded. Processing loaded papers...")

    for idx, paper in enumerate(author.getPapers()):
        paper_authors = paper.getInfo()['Authors'].lower()
        fname = author.getFirstName()
        lname = author.getLastName()

        if (paper_authors.find(fname) == -1 or paper_authors.find(lname) == -1):
            print('Error: author: ' + fname + ' ' + lname + ' is not a valid author of this paper.')
            return -1

        auth_word = get_ref_author_format(fname, lname, paper.getInfo()['Publisher'])

        analyzer = PaperReferenceExtractor()

        pdf_paper = paper.getPdfObj()
        if (pdf_paper is None):
            print('No PDF object for this paper, skipping.')
            continue
        refContent = analyzer.getReferencesContent(pdf_paper)

        if (refContent is not None):

            numCites = analyzer.getCitesToAuthor(auth_word, refContent)
            #print (fname+ ' '+lname+ ' has '+str(numCites)+' number of self-cites in paper: '+ paper.getInfo()['Title'])
            self_cites_info = {'Paper Title': paper.getInfo()['Title'], 'Self Cites': numCites}
        else:
            self_cites_info = {'Paper Title': paper.getInfo()['Title'], 'Self Cites': 'No Valid PDF CONTENT in GSC'}

        print('Paper ' + str(idx) + ' complete.')
        print(self_cites_info)
        self_cite_arr.append(self_cites_info)

    return self_cite_arr


#given an author, and a number of papers, returns the journal frequency list of the first 30 citing papers
def count_journal_frequency (author, num_papers):

    author.loadPapers(num_papers)
    print("Author fully loaded. Processing loaded papers...")
    pap_arr = []

    for idx, paper in enumerate(author.getPapers()):
        info_list = []
        one_pap_arr = []
        cited_by_url = paper.getCitedByUrl()
        session = requests.Session()

        url_part_one = 'https://scholar.google.ca/scholar?start='
        url_part_two = '&hl=en&as_sdt=0,5&sciodt=0,5&cites='
        cited_by_url = cited_by_url[:cited_by_url.rfind('&')]
        paper_code = cited_by_url[cited_by_url.rfind('=')+1:]

        for i in range(10, 31, 10):
            time.sleep(10)
            final_url = url_part_one+str(i)+url_part_two+paper_code
            response = session.get(final_url)
            soup = BeautifulSoup(response.content, "lxml")
            info_list += soup.findAll('div', attrs={'class':'gs_a'})

        journal_dict = {}

        for info_str in info_list:
            info_str = info_str.text
            info_str = info_str.split('-')[1].split(',')[0]
            #print('final info string: ' + info_str)

            if (info_str in journal_dict):
                journal_dict[info_str]+=1
            else:
                journal_dict[info_str] = 1

        one_pap_arr.append(paper.getInfo()['Title']) 
        one_pap_arr.append(journal_dict)
        print(one_pap_arr)
        pap_arr.append(one_pap_arr)
        print('Paper ' + str(idx) + ' complete.')

    return pap_arr


# given an author, takes x_most_rel number of papers and finds the top_x most cited authors, with total citation count
# then, takes each of those authors, and determines how many times they cite the given author in their x_most_rel number of papers
def count_cross_cites (author, x_most_rel, top_x):
    author.loadPapers(x_most_rel)
    paper_list = author.getPapers()
    ORIG_FNAME = author.getFirstName()
    ORIG_LNAME = author.getLastName()
    print("Total number of valid GSC papers: " + str(len(paper_list)))
    citation_list= []

    ref_processor = PaperReferenceExtractor()
    springer_bot = SpringerReferenceParser()
    ieee_bot = IeeeReferenceParser()

    # gets all the citations from all the papers in the list
    for paper in paper_list:
        pub = paper.getInfo()['Publisher']
        pdf_paper = paper.getPdfObj()
        if (pdf_paper is None):
            continue

        try:
            ref_content = ref_processor.getReferencesContent(pdf_paper)
            if (ref_content is None):
                continue
        except TypeError as e:
            print('weird ord() error: ')
            print(e)
            continue
        except PyPDF2.utils.PdfReadError as e:
            print(e)
            continue

        if (pub == 'IEEE'):
            citations = ieee_bot.citeParse(ref_content)
        elif (pub == 'Springer US'):
            citations = springer_bot.citeParse(ref_content)
        else:
            print('Invalid publication format from: ' + pub)
            return -1

        citation_list += citations

    print('From the valid top ' + str(top_x) +' papers, all the citations found: ' + str(citation_list))

    author_dist = {}

    #goes through each citation and takes out authors and paper names and puts it in the valid frequency dictionary
    # end results: {'author': {'freq': int frequency original author cites him, 'paper': [array of paper titles in which the cited author is cited]}, 
    for citation in citation_list:
        title = citation['title']
        for cited_author in citation['authors']:
            if cited_author in author_dist:
                author_dist[cited_author]['freq'] += 1
                if title not in author_dist[cited_author]['papers']:
                    author_dist[cited_author]['papers'].append(title)
            else:
                author_dist[cited_author] = {}
                author_dist[cited_author]['freq'] = 1
                author_dist[cited_author]['papers'] = [title]

    print('unsorted author list: ' + str(author_dist))

    #sorts the dictionary - now an array of tuples that are sorted by frequency
    #author_dist should be in the form [('author', {'freq': 5, 'papers':[]}), ...]
    author_dist = list(reversed(sorted(author_dist.items(), key=lambda x: x[1]['freq'])))

    print('sorted author list in tuples: ' + str(author_dist))

    gsc_bot = GscHtmlFunctions()
    top_x_authors = []

    #this part will create valid author objects for each of the top cited authors and append it to a list
    for index, author_info in enumerate(author_dist):

        time.sleep(5)

        if (index > top_x - 1):
            break

        #author info should be in the form ('author', {'freq': 5, 'papers':[]})
        first_paper_title = author_info[1]['papers'][0]
        frequency = author_info[1]['freq']
        author_name = author_info[0]
        returned_author = gsc_bot.get_author_from_search(author_name, first_paper_title)
        if returned_author is -1:
            #if can't find gsc profile for author, go onto the next top cited author
            top_x += 1
        else:
            #each value is an array of two values: author object, and frequency cited
            top_x_authors.append([returned_author, returned_author.getFirstName(), returned_author.getLastName(), frequency])

    print('Top citing authors: ')
    print(top_x_authors)

    #gets number of times each of these authors cites the original author

    # array to store another array of author, and how many times they cite the original author
    cited_author_info_arr = []

    for cited_author_freq_arr in top_x_authors:
        time.sleep(5)
        top_cited_author = cited_author_freq_arr[0]
        top_cited_author.loadPapers(x_most_rel)

        cited_fname = top_cited_author.getFirstName()
        cited_lname = top_cited_author.getLastName()

        temp_paper_lst = top_cited_author.getPapers()
        total_cites = 0

        #determines number of times the paper cites the original author
        for paper in temp_paper_lst:
            pdf_paper = paper.getPdfObj()
            if (pdf_paper is None):
                continue
            analyzer = PaperReferenceExtractor()
            try:
                content = analyzer.getReferencesContent(pdf_paper)
                if (content is None):
                    continue
            except TypeError as e:
                print('weird ord() error: ')
                print(e)
                continue
            except PyPDF2.utils.PdfReadError as e:
                print(e)
                continue

            auth_word = get_ref_author_format(cited_fname, cited_lname, paper.getInfo()['Publisher'])
            total_cites += analyzer.getCitesToAuthor(auth_word, content)

        cited_author_info_arr.append([top_cited_author, cited_fname, cited_lname, total_cites])

    print('cited_author_info_arr: ' + str(cited_author_info_arr))

    #compilation of all the information
    final_info_dict = {'First Name': ORIG_FNAME, 'Last Name': ORIG_LNAME, 'Author_citation_frequency': top_x_authors, 'Cited_authors_overcite_frequency': cited_author_info_arr}

    return final_info_dict



#getting more recent papers from vasilakos over cite data

# try:
#     vas = AcademicPublisher('https://scholar-google-ca.proxy.lib.uwaterloo.ca/citations?hl=en&user=_yWPQWoAAAAJ&view_op=list_works&sortby=pubdate', 80, loadPaperPDFs=False)
#     over_cite_arr = []
#     for paper in vas.getPapers():
#         if (paper.getCitedByUrl() is not None and paper.getCitedByNum()>=40):
#             paper.setPdfObj()
#             arr = count_overcites(paper, vas)
#             k = "Paper Title: " + paper.getInfo()['Title']
#             arr.append(k)
#             over_cite_arr.append(arr)
#             print(arr)
#     over_cite_writer(over_cite_arr, 'vas_most_recent_overcites')
# except AttributeError as e:
#     print('google scholar has blocked you.')
#     print(e)

