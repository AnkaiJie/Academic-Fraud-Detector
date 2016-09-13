
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import scrapper

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

#self cites
# vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1, loadPaperPDFs=False)
# self_cite_arr = count_self_cites(vas, 50)
# self_cite_writer(self_cite_arr, 'data/vas_top50_self_cites2')


#getting bare data from more relevant papers
# vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1, loadPaperPDFs=False)
# over_cite_arr = count_overcites(vas, 50)
# over_cite_writer(over_cite_arr, 'rel_idx_5')

#Journal Cites
# vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1, loadPaperPDFs=False)
# journal_cite_arr = count_journal_frequency(vas, 50)
# jounal_dict_writer(journal_cite_arr, 'vas_top50_journals_freq')


# p = Paper(SessionInitializer.ROOT_URL+'/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&cstart=20&pagesize=80&citation_for_view=_yWPQWoAAAAJ:Xz60mAmATU4C')
# vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1, loadPaperPDFs=False)
# print(count_overcites_paper(p, vas, cite_num_to_load=30))


# vas = AcademicPublisher(SessionInitializer.ROOT_URL + '/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1)
# cross_cite_dict = count_cross_cites(vas, 50, 11, 50)
# #cross_cite_dict = count_cross_cites_stage3(vas, stage2.k, 1, 1, 2)
# cross_cite_writer(cross_cite_dict, 'vas_top50_cross_cites')