
from scrapper import *
from csvWriter import *

#recent overcites
def author_overcites_recent(link, name):
	auth = AcademicPublisher(SessionInitializer.ROOT_URL + link, 100, loadPaperPDFs=False)
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
	auth = AcademicPublisher(SessionInitializer.ROOT_URL + link, 1, loadPaperPDFs=False)
	self_cite_arr = count_self_cites(auth, num)
	self_cite_writer(self_cite_arr, 'data/' + name + '/' + name + '_top_' + str(num) + '_selfcites')


# getting bare data from more relevant papers
def author_overcites(link, name, num):
	auth = AcademicPublisher(SessionInitializer.ROOT_URL + link, 1, loadPaperPDFs=False)
	over_cite_arr = count_overcites(auth, num)
	over_cite_writer(over_cite_arr, 'data/' + name + '/' + name + '_top_' + str(num) + '_selfcites')


# Journal Cites
def author_journalfreq(link, name, num):
	auth = AcademicPublisher(SessionInitializer.ROOT_URL + link, 1, loadPaperPDFs=False)
	journal_cite_arr = count_journal_frequency(auth, num)
	jounal_dict_writer(journal_cite_arr, 'data/' + name + '/' + name + '_top_' + str(num) + '_jounalfreq')


def author_crosscites(link, name):
	auth = AcademicPublisher(SessionInitializer.ROOT_URL + link, 1)
	cross_cite_dict = count_cross_cites(auth, 50, 11, 50)
	cross_cite_writer(cross_cite_dict, 'data/' + name + '/' + name + '_top_' + str(num) + '_crosscites')


#Vasilakos
# author_overcites('/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 'vasilakos', 50)