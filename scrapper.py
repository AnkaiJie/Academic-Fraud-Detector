
'''
Created on Jan 7, 2016

@author: Ankai
'''

from academicThings import AcademicPublisher, GscHtmlFunctions, Paper
from academicThings import GscPdfExtractor
from ReferenceParser import PaperReferenceExtractor, SpringerReferenceParser, IeeeReferenceParser
from bs4 import BeautifulSoup
import requests
import time
import PyPDF2
import SessionInitializer
from csvWriter import *
import stage2


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
            return None

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
        time.sleep(10)
        info_list = []
        one_pap_arr = []
        cited_by_url = paper.getCitedByUrl()
        session = requests.Session()

        url_part_one = SessionInitializer.ROOT_URL + '/scholar?start='
        url_part_two = '&hl=en&as_sdt=0,5&sciodt=0,5&cites='
        cited_by_url = cited_by_url[:cited_by_url.rfind('&')]
        paper_code = cited_by_url[cited_by_url.rfind('=')+1:]

        for i in range(0, 30, 10):
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
        return None


# given an author, takes x_most_rel number of papers and finds the top_x most cited authors, with total citation count
# then, takes each of those authors, and determines how many times they cite the given author in their y_most_rel number of papers
def count_cross_cites (author, x_most_rel, top_x, y_most_rel):
    author.loadPapers(x_most_rel, pubFilter=True, delay=True)
    paper_list = author.getPapers()
    x_most_rel = len(paper_list)
    ORIG_FNAME = author.getFirstName()
    ORIG_LNAME = author.getLastName()
    print("Total number of valid GSC papers: " + str(len(paper_list)))
    citation_list = []

    springer_bot = SpringerReferenceParser()
    ieee_bot = IeeeReferenceParser()

    # gets all the citations from all the papers in the list
    print('STAGE 1 GETTING CITATIONS')
    print("-----------------------------------------------------------")
    for paper in paper_list:
        pub = paper.getInfo()['Publisher']
        pdf_paper = paper.getPdfObj()
        print('Paper title: ' + str(paper.getInfo()['Title']))
        if (pdf_paper is None):
            print('paper object is none')
            continue

        extractor = PaperReferenceExtractor()
        ref_content = extractor.getReferencesContent(pdf_paper)

        if (ref_content is None):
            continue
        try:
            if (pub == 'IEEE'):
                citations = ieee_bot.citeParse(ref_content)
            elif (pub == 'Springer US'):
                citations = springer_bot.citeParse(ref_content)
            else:
                print('Invalid publication format from: ' + pub)
                continue
        except Exception as e:
            print('An exception occured with parsing citations: ' + str(e))

        citation_list += citations
    print("STAGE 1 COMPLETE -----------------------------------------------------------")
    print('From the valid top ' + str(top_x) +' papers, all the citations found: ' + str(citation_list))

    author_dist = {}

    #goes through each citation and takes out authors and paper names and puts it in the valid frequency dictionary
    # end results: {'author': {'freq': int frequency original author cites him, 'paper': [array of paper titles in which the cited author is cited]}, 
    print('STAGE 2 AGGREGATING CITATION COUNTS BY AUTHOR ------------------------------------')

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


    #sorts the dictionary - now an array of tuples that are sorted by frequency
    #author_dist should be in the form [('author', {'freq': 5, 'papers':[]}), ...]
    author_dist = list(reversed(sorted(author_dist.items(), key=lambda x: x[1]['freq'])))
    print('STAGE 2 COMPLETE -----------------------------------------------------------------')
    print('sorted author list in tuples: ' + str(author_dist))

    count_cross_cites_stage3(author, author_dist, x_most_rel, top_x, y_most_rel)



def count_cross_cites_stage3(orig_author, author_dist, x_most_rel, top_x, y_most_rel):
    gsc_bot = GscHtmlFunctions()
    top_x_authors = []
    print('STAGE 3 CREATING NEW AUTHOR OBJECTS ---------------------------------------------------------')
    #this part will create valid author objects for each of the top cited authors and append it to a list
    for index, author_info in enumerate(author_dist):

        time.sleep(10)

        if (index > top_x - 1):
            break

        #author info should be in the form ('author', {'freq': 5, 'papers':[]})
        first_paper_title = author_info[1]['papers'][0]
        frequency = author_info[1]['freq']
        author_name = author_info[0]
        print('Trying to find author: ' + str(author_info))
        returned_author = gsc_bot.get_author_from_search(author_name, first_paper_title)
        if returned_author is None:
            #if can't find gsc profile for author, go onto the next top cited author
            top_x += 1
        else:
            #each value is an array of two values: author object, and frequency cited
            top_x_authors.append([returned_author, returned_author.getFirstName(), returned_author.getLastName(), frequency])
    print('DONE STAGE 3 --------------------------------------------------------------------------')
    print('Top citing authors: ')
    print(top_x_authors)

    print('STAGE 4 COUNTING NUMBER OF CITATIONS TO ORIGINAL AUTHOR --------------------------------')
    #gets number of times each of these authors cites the original author

    # array to store another array of author, and how many times they cite the original author
    cited_author_info_arr = []
    ORIG_FNAME = orig_author.getFirstName()
    ORIG_LNAME = orig_author.getLastName()

    for cited_author_freq_arr in top_x_authors:
        time.sleep(5)
        top_cited_author = cited_author_freq_arr[0]
        top_cited_author.loadPapers(y_most_rel, pubFilter=True, delay=True)

        cited_fname = top_cited_author.getFirstName()
        cited_lname = top_cited_author.getLastName()

        print('ANALYZING AUTHOR: ' + str(cited_fname) + ' ' + str(cited_lname))

        temp_paper_lst = top_cited_author.getPapers()
        pap_list_len = len(temp_paper_lst)
        total_paper_cites = []

        #determines number of times the paper cites the original author
        for paper in temp_paper_lst:
            pap_title = paper.getInfo()['Title']
            print('Paper title: ' + pap_title)
            auth_word = get_ref_author_format(ORIG_FNAME, ORIG_LNAME, paper.getInfo()['Publisher'])
            pdf_paper = paper.getPdfObj()
            if (pdf_paper is None):
                print('paper object is none')
                continue
            analyzer = PaperReferenceExtractor()

            content = analyzer.getReferencesContent(pdf_paper)
            if (content is None):
                continue
            elif auth_word is None:
                print('for some reason, authword is none. Shouldnt be happening')
                continue

            num_cites = analyzer.getCitesToAuthor(auth_word, content)
            total_paper_cites.append([pap_title, num_cites])


        cited_author_info_arr.append([top_cited_author, cited_fname, cited_lname, total_paper_cites, pap_list_len])
    print('STAGE 4 COMPLETE ---------------------------------------------------------------------')
    print('cited_author_info_arr: ' + str(cited_author_info_arr))


    print('FINAL INFO DICTIONARY -------------------------------------------------------------')
    #compilation of all the information
    final_info_dict = {'First Name': ORIG_FNAME, 'Last Name': ORIG_LNAME, 
    'Author_citation_frequency': top_x_authors, 'Cited_authors_overcite_frequency': cited_author_info_arr,
    'x_most_rel': x_most_rel, 'y_most_rel': y_most_rel}
    print(final_info_dict)
    return final_info_dict



# given paper and author, and index number, returns number of times a each
# citing paper on the first page of citing papers also cites the same author
def count_overcites(author, auth_paper_num, cite_num_to_load=30, recent=False):
    over_cite_arr = []
    author.loadPapers(auth_paper_num, loadPaperPDFs=False, pubFilter=False)
    count = 0
    try:
        for paper in vas.getPapers():
            if paper.getCitedByUrl() is None:
                print("No cited by url for paper: " + paper.getInfo()['Title'] + "with link " + paper.getUrl() + ", loop continue called")
                continue
            time.sleep(30)
            #paper.setPdfObj()
            k = "Paper Title: " + paper.getInfo()['Title']
            print(k)
            arr = count_overcites_paper(paper, vas, cite_num_to_load=cite_num_to_load)
            arr.append(k)
            over_cite_arr.append(arr)
            print(arr)
            count+=1
    except Exception:
        print('returning back over_cite_arr')

    print(str(count) + "number of papers analyzed")
    print(over_cite_arr)
    return over_cite_arr


# this function takes a paper instead of an author, leaves the author implementation to the user
# use case: allows used to only look at overcites for specific papers
def count_overcites_paper(paper, author, cite_num_to_load=30):
    try:
        pdfExtractor = GscPdfExtractor()

        cited_by_url = paper.getCitedByUrl()
        url_part_one = SessionInitializer.ROOT_URL + '/scholar?start='
        url_part_two = '&hl=en&as_sdt=0,5&sciodt=0,5&cites='
        cited_by_url = cited_by_url[:cited_by_url.rfind('&')]
        paper_code = cited_by_url[cited_by_url.rfind('=')+1:]

        all_pdfObjs = []
        overcites_info = []

        print('-----------------------------------LOADING CITING PAPERS-----------------------------------')
        for i in range (0, cite_num_to_load, 10):
            time.sleep(10)
            final_url = url_part_one+str(i)+url_part_two+paper_code
            print('page url for citations:')
            print(final_url)
            current_pdfObjs = pdfExtractor.findPapersFromCitations(final_url)
            all_pdfObjs += current_pdfObjs

        print('-----------------------------------DONE CITING PAPERS-------------------------------------')

        print('Loaded: ' + str(len(all_pdfObjs)) + ' pdf objects.')

        analyzer = PaperReferenceExtractor()

        for idx, pdf in enumerate(all_pdfObjs):
            content = analyzer.getReferencesContent(pdf)
            title = pdf.getTitle()
            
            if content is None and title is not None:
                print("Citing paper number " + str(idx+1) + ": " + title + " had no PDF content found.")
                info_dict = {}
                info_dict['Citing Paper Number'] = idx+1
                info_dict['Title'] = title
                info_dict['Over-cite Count'] = "No PDF Found"
                overcites_info.append(info_dict)
                continue
            elif content is None:
                continue
                
            # print(content)
            lname = author.getLastName().title()
            numCites = analyzer.getCitesToAuthor(lname, content)
            if title is None:
                title = 'Unknown Title'
            print("Citing paper number " + str(idx+1) + ": " + title + " cites " + lname + " " + str(numCites) + " times.")
            info_dict = {}
            info_dict['Citing Paper Number'] = idx+1
            info_dict['Title'] = title
            info_dict['Over-cite Count'] = numCites
            overcites_info.append(info_dict)

    except AttributeError as e:
        print('google scholar possibly has blocked you, sending back collected data...')
        print(e)
        return overcites_info
    except Exception as e:
        print('unknown exception ' + str(e))
        return overcites_info

    return overcites_info




#getting more recent papers from vasilakos over cite data

# vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?hl=en&user=_yWPQWoAAAAJ&view_op=list_works&sortby=pubdate', 100, loadPaperPDFs=False)
# over_cite_arr = []
# for paper in vas.getPapers():
#     if paper.getInfo()['Title'] == 'Delay tolerant networks: Protocols and applications':
#         continue
#     if (paper.getCitedByUrl() is not None and paper.getCitedByNum()>=30):
#         time.sleep(30)
#         paper.setPdfObj()
#         arr = count_overcites_paper(paper, vas)
#         k = "Paper Title: " + paper.getInfo()['Title']
#         arr.append(k)
#         over_cite_arr.append(arr)
#         print(arr)
# over_cite_writer(over_cite_arr, 'vas_most_recent_overcites5')

# getting bare data from more relevant papers
# vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1, loadPaperPDFs=False)
# over_cite_arr = count_overcites(vas, 50)
# over_cite_writer(over_cite_arr, 'most_rel_overcites_idx24')


# p = Paper(SessionInitializer.ROOT_URL+'/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&cstart=20&pagesize=80&citation_for_view=_yWPQWoAAAAJ:Xz60mAmATU4C')
# vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1, loadPaperPDFs=False)
# print(count_overcites_paper(p, vas, cite_num_to_load=30))


vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1)
# cross_cite_dict = count_cross_cites(vas, 50, 10, 50)
cross_cite_dict = count_cross_cites_stage3(vas, stage2.k, 50, 10, 50)
cross_cite_writer(cross_cite_dict, 'vas_top50_cross_cites')

