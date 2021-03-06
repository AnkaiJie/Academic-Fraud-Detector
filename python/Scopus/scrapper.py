
'''
Created on Jan 7, 2016

@author: Ankai
'''

from ScopusParse import AcademicPublisher, Paper
from ReferenceParser import PaperReferenceExtractor, SpringerReferenceParser, IeeeReferenceParser
from bs4 import BeautifulSoup
import WatLibSeleniumParser

# given a paper, counts the number of times it cites an author of the paper
def count_self_cites(author, num_load):
    author.loadPapers(num_load, loadPaperPDFs=False)
    self_cite_arr = []
    print("Author fully loaded. Processing loaded papers...")

    try:
        for idx, paper in enumerate(author.getPapers()):
            #auth_word = get_ref_author_format(fname, lname, paper.getInfo()['Publisher'])
            auth_word = author.getLastName().title()


            title = paper.getInfo()['title']
            print('Paper title: ' + str(title))
            paper.setPdfObj()

            analyzer = PaperReferenceExtractor()

            pdf_paper = paper.getPdfObj()
            if (pdf_paper is None):
                print('No PDF object for this paper, skipping.')
                self_cite_arr.append({'Paper Title': title, 'Self Cites': 'No PDF found'})
                continue
            refContent = analyzer.getReferencesContent(pdf_paper)

            num_cites = 0
            if (refContent is not None):

                num_cites = analyzer.getCitesToAuthor(auth_word, refContent)
                #print (fname+ ' '+lname+ ' has '+str(numCites)+' number of self-cites in paper: '+ paper.getInfo()['Title'])
                self_cites_info = {'Paper Title': title, 'Self Cites': num_cites}
            else:
                self_cites_info = {'Paper Title': title, 'Self Cites': 'No PDF found'}

            print('Paper title: ' + str(title) + ' has self cites: ' + str(num_cites))
            self_cite_arr.append(self_cites_info)

        
    except KeyboardInterrupt:
        print('key board KeyboardInterrupt returninbg self cite array')

    print(self_cite_arr)
    return self_cite_arr



# given paper and author, and index number, returns number of times a each
# citing paper on the first page of citing papers also cites the same author
def count_overcites(author, auth_paper_num, startidx, endidx, cite_num_to_load=40):
    over_cite_arr = []
    author.loadPapers(auth_paper_num, loadPaperPDFs=False)
    count = 0
    try:
        for paper in author.getPapers()[startidx:endidx]:
            if paper.getCitedByUrl() is None:
                print("No cited by url for paper: " + paper.getInfo()['Title'] + "with link " + paper.getUrl() + ", loop continue called")
                continue
            #paper.setPdfObj()
            k = "Paper Title: " + paper.getInfo()['title']
            print(k)
            arr = count_overcites_paper(paper, author, cite_num_to_load=cite_num_to_load)
            arr.append(k)
            over_cite_arr.append(arr)
            print("PAPER ARRAY DICT")
            print(arr)
            count+=1
    except AttributeError:
        print('google scholar possibly has blocked you, sending back collected data...')
    except KeyboardInterrupt:
        print('User ended program, returning over cite array')

    print(str(count) + " number of papers analyzed")
    print(over_cite_arr)
    return over_cite_arr


# this function takes a paper instead of an author, leaves the author implementation to the user
# use case: allows used to only look at overcites for specific papers
def count_overcites_paper(paper, author, cite_num_to_load=40):
    overcites_info = []
    try:
        all_pdfObjs = paper.getCitingPdfs(cite_num_to_load)

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

    except KeyboardInterrupt:
        print('User ended program. Returning existing Data')
        WatLibSeleniumParser.reset()
        return overcites_info

    return overcites_info

