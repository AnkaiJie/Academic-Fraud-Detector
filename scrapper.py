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
import time
import PyPDF2
from _csv import Error
import traceback
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
    pdfUrls = pdfExtractor.findPapersFromCitations(paper.getCitedByUrl())
    # print(pdfUrls)
    analyzer = PaperReferenceExtractor()
    overcites_info = []
    
    for idx, pdf in enumerate(pdfUrls):
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
    for paper in author.getPapers():
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

        pdfUrl = paper.getPdfUrl()
        if (pdfUrl is None):
            print('No PDF url for this paper, skipping.')
            continue
        refContent = analyzer.getReferencesContent(pdfUrl)

        if (refContent is not None):

            numCites = analyzer.getCitesToAuthor(auth_word, refContent)
            #print (fname+ ' '+lname+ ' has '+str(numCites)+' number of self-cites in paper: '+ paper.getInfo()['Title'])
            self_cites_info = {'Paper Title': paper.getInfo()['Title'], 'Self Cites': numCites}
        else:
            self_cites_info = {'Paper Title': paper.getInfo()['Title'], 'Self Cites': 'No Valid PDF URL in GSC'}

        print(self_cites_info)
        self_cite_arr.append(self_cites_info)

    return self_cite_arr

#given an author, and a number of papers, returns the journal frequency list of the first 30 citing papers
def count_journal_frequency (author, num_papers):

    author.loadPapers(num_papers);
    pap_arr = []
    
    for paper in author.getPapers():
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
        pdfurl = paper.getPdfUrl()
        if (pdfurl is None):
            continue
        print('pdfUrl ' + pdfurl)
        
        try:
            ref_content = ref_processor.getReferencesContent(pdfurl)
            if (ref_content is None):
                continue
        except TypeError as e:
            print('weird ord() error: ')
            print(e)
            continue
        except PyPDF2.utils.PdfReadError as e:
            print(e)
            continue
        
        
        if (pub=='IEEE'):
            citations = ieee_bot.citeParse(ref_content)
        elif (pub=='Springer US'):
            citations = springer_bot.citeParse(ref_content)
        else:
            print('Invalid publication format from: '+pub)
            return -1
        
        citation_list += citations  
    
    print('From the valid top '+ str(top_x) +' papers, all the citations found: '+ str(citation_list))
    
    
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
    for index, author_info in enumerate (author_dist):
        
        time.sleep(5)
        
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
            if (paper.getPdfUrl() is None):
                continue
            analyzer = PaperReferenceExtractor()
            try:
                content = analyzer.getReferencesContent(paper.getPdfUrl())
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
    
    print('cited_author_info_arr: '+ str(cited_author_info_arr))
    
    #compilation of all the information
    final_info_dict = {'First Name': ORIG_FNAME,'Last Name': ORIG_LNAME, 'Author_citation_frequency': top_x_authors, 'Cited_authors_overcite_frequency':cited_author_info_arr}
    
    return final_info_dict



print('Academic Fraud Detector')
authorlink = input('Please enter the Google Scholar profile link of the author you want to investigate:\n')
entered_author = AcademicPublisher(authorlink,1)

while 1:
    function_select = input('Please select the function you want to run on this author. Enter 1 for self-cites, 2 for over-cites,\n'
                            '3 for cross-cites, and 4 for journal frequency. Enter anything else to exit program.\n')
    if(function_select=='1'):
        pap_num = int(input('Self-cites selected. Enter the number of papers you want to load:\n'))
        csv_file_name = input('Do you want to output your result into a csv file?\nIf yes, enter the name of the file. If no, enter "n".\n')
        entered_author.loadPapers(pap_num)
        self_cite_arr = count_self_cites(entered_author, pap_num)
        print(self_cite_arr)
        if (csv_file_name != 'n'):
            self_cite_writer(self_cite_arr, csv_file_name)

    elif (function_select=='2'):
        pap_num = int(input('Over-cites selected. Enter the number of papers you want to load:\n'))
        csv_file_name = input('Do you want to output your result into a csv file?\nIf yes, enter the name of the file. If no, enter "n".\n')

        entered_author.loadPapers(pap_num)
        over_cite_arr = []
        try:

            for paper in entered_author.getPapers():
                arr = count_overcites(paper, entered_author)
                k = "Paper Title: " + paper.getInfo()['Title']
                arr.append(k)
                over_cite_arr.append(arr)
                print(arr)
            print(over_cite_arr)
        except AttributeError as e:
            print('google scholar has blocked you.')
            print(e)

        if (csv_file_name != 'n'):
            over_cite_writer(over_cite_arr, csv_file_name)

    elif (function_select=='3'):
        x_most_rel = int(input('Cross-cites selected. Enter the number of papers you want to load for the authors:\n'))
        auth_num = int(input('Enter the number of cited authors you want to analyze:\n'))
        try:
            print(count_cross_cites(entered_author, x_most_rel, auth_num))
            print('FINAL RESULT')
        except Error as e:
            print(e)
        except Exception as e:
            print(e)
        except AttributeError as e:
            print(e)
            traceback.print_exc()

    elif (function_select == '4'):
        pap_num = int(input('Journal frequency selected. Enter the number of papers you want to load:\n'))
        csv_file_name = input('Do you want to output your result into a csv file?\nIf yes, enter the name of the file. If no, enter "n".\n')
        journal_dict_arr = []
        try:
            journal_dict_arr = count_journal_frequency(entered_author, pap_num)
            print(journal_dict_arr)
            print('Journal Dict array')
        except AttributeError as e:
            print(e)
            traceback.print_exc()

        if (csv_file_name != 'n'):
            jounal_dict_writer(journal_dict_arr, csv_file_name)

    else:
        break

'''
#Cross_cites script for top 10 papers for Vasilakos 
try:
    vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1)
    time.sleep(5)
    print('FINAL RESULT: ' + str(count_cross_cites(vas, 10, 5)))
except Error as e:
    print(e)
except Exception as e:
    print(e)
except AttributeError as e:
    print(e)
    traceback.print_exc()
'''

'''
#Self cites script for top 15 papers of vasilakos
vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 15)
for paper in vas.getPapers():
    print(count_self_cites(vas, paper))
'''

'''
#Over cites script for top 15 papers of vasilakos
try:
    vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 15)
    print(str(len(vas.getPapers())))
    time.sleep(10)
    for paper in vas.getPapers()[8:]:
        arr = count_overcites(paper, vas)
        k = "Paper Title: " + paper.getInfo()['Title']
        arr.append(k)
        print(arr)
except AttributeError as e:
    print('google scholar has blocked you.')
    print(e)
'''
'''
try:
    vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1)
    time.sleep(5)
    print('Journal Dict array ' + str(count_journal_frequency(vas, 15)))
except AttributeError as e:
    print(e)
    traceback.print_exc()
'''

#getting more recent papers from vasilakos over cite data
'''
try:
    vas = AcademicPublisher('https://scholar.google.ca/citations?hl=en&user=_yWPQWoAAAAJ&view_op=list_works&sortby=pubdate', 80)
    time.sleep(10)
    for paper in vas.getPapers():
        if (paper.getCitedByUrl() is not None and paper.getCitedByNum()>=50):
            arr = count_overcites(paper, vas)
            k = "Paper Title: " + paper.getInfo()['Title']
            arr.append(k)
            print(arr)
except AttributeError as e:
    print('google scholar has blocked you.')
    print(e)
'''
