
from scrapper import *
from csvWriter import *

#recent overcites
def author_overcites_recent(link, name):
    auth = AcademicPublisher(link, 100, loadPaperPDFs=False)
    over_cite_arr = []
    for paper in auth.getPapers():
        if (paper.getCitedByUrl() is not None and paper.getCitedByNum()>=30):
            time.sleep(30)
            paper.setPdfObj()
            arr = count_overcites_paper(paper, auth)
            k = "Paper Title: " + paper.getInfo()['Title']
            arr.append(k)
            over_cite_arr.append(arr)
            print(arr)
    over_cite_writer(over_cite_arr, 'data/' + name + '/' + name + 'most_recent_overcites')

# self cites
def author_selfcites(link, name, num):
    auth = AcademicPublisher(link, 1, loadPaperPDFs=False)
    self_cite_arr = count_self_cites(auth, num)
    self_cite_writer(self_cite_arr, 'data/' + name + '/' + name + '_top_' + str(num) + '_selfcites')


# getting bare data from more relevant papers
def author_overcites(link, name, num, sortType='relevance'):
    auth = AcademicPublisher(link, 1, loadPaperPDFs=False, sortType=sortType)
    over_cite_arr = count_overcites(auth, num)
    over_cite_writer(over_cite_arr, 'data/' + name + '/' + name + '_top_' + str(num) + '_overcites_' + sortType)


# Journal Cites
def author_journalfreq(link, name, num):
    auth = AcademicPublisher(link, 1, loadPaperPDFs=False)
    journal_cite_arr = count_journal_frequency(auth, num)
    jounal_dict_writer(journal_cite_arr, 'data/' + name + '/' + name + '_top_' + str(num) + '_journalfreq')
    #total_journal_dict_writer(journal_cite_arr, 'data/' + name + '/' + name + '_top_' + str(num) + '_totaljournalfreq')


def author_crosscites(link, name):
    auth = AcademicPublisher(link, 1)
    cross_cite_dict = count_cross_cites(auth, 50, 11, 50)
    cross_cite_writer(cross_cite_dict, 'data/' + name + '/' + name + '_top_' + str(num) + '_crosscites')


#Vasilakos
author_overcites('https://www-scopus-com.proxy.lib.uwaterloo.ca/authid/detail.uri?origin=resultslist&authorId=22954842600&zone=', 'vasilakos', 5)
#author_overcites('https://www-scopus-com.proxy.lib.uwaterloo.ca/authid/detail.uri?origin=resultslist&authorId=22954842600&zone=', 'vasilakos', 50, sortType='date')

#Abdelzaher
#author_overcites ('/citations?user=cA28Zs0AAAAJ&hl=en&oi=ao', 'abdelzaher', 3)
#author_journalfreq('/citations?user=cA28Zs0AAAAJ&hl=en&oi=ao', 'abdelzaher', 50)
#author_selfcites('/citations?user=cA28Zs0AAAAJ&hl=en&oi=ao', 'abdelzahers', 50)
# author_overcites_recent('/citations?user=cA28Zs0AAAAJ&hl=en&oi=ao', 'abdelzaher')
# author_crosscites('/citations?user=cA28Zs0AAAAJ&hl=en&oi=ao', 'abdelzaher' )