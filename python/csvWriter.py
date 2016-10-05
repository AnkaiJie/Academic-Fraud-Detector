# -*- coding: utf-8 -*-

import csv


'''
Created on Jan 05, 2016

@author: Ankai

'''

def total_journal_dict_writer (journal_dict,name):

    total_journal_dict = {}

    for paper in journal_dict:
        for title, count in paper[1].items():
            title = title.lower().title()
            if title in total_journal_dict:
                total_journal_dict[title] += count
            else:
                total_journal_dict[title] = count

    writer = csv.writer(open(name+'.csv', 'w', newline=''))
    writer.writerow(['Journal', 'Total Citing Papers from Journal'])
    for key, value in total_journal_dict.items():
        try:
            writer.writerow([key, value])
        except UnicodeEncodeError:
            continue


def jounal_dict_writer(indJournalArrays, name):
    writer = csv.writer(open(name + '.csv', 'w'), lineterminator='\n')
    for paper in indJournalArrays:
        writer.writerow(['Paper Title: ' + paper[0]])
        for key, value in paper[1].items():
            try:
                writer.writerow([key, value])
            except UnicodeEncodeError:
                continue
        writer.writerow(['\n'])



def self_cite_writer(self_cite_arr, name):
    writer = csv.writer(open(name + '.csv', 'w'), lineterminator='\n')
    writer.writerow(["Paper Title", "Self Cite Count"])
    for paper in self_cite_arr:
        writer.writerow([paper['Paper Title'], paper['Self Cites']])



def over_cite_writer(over_cite_arr, name):

    writer = csv.writer(open(name + '.csv', 'w'), lineterminator='\n')
    for paper in over_cite_arr:

        writer.writerow([paper[-1]])
        headers =['Citing Paper Number', 'Paper Title', 'Over-cite Count']
        writer.writerow(headers)
        paper.pop()
        total =0
        for dict_item in paper:
            writer.writerow([dict_item['Citing Paper Number'], dict_item['Title'], dict_item['Over-cite Count']])
            if dict_item['Over-cite Count'] != "No PDF Found":
                    total+=dict_item['Over-cite Count']
        writer.writerow(['', 'Total', total])
        writer.writerow(['\n'])

def cross_cite_writer(cross_cite_dict, name):
    x_most_rel = cross_cite_dict['x_most_rel']

    writer = csv.writer(open(name + '.csv', 'w'), lineterminator='\n')

    orig_name = cross_cite_dict['First Name'].title() + ' ' + cross_cite_dict['Last Name'].title()
    writer.writerow([orig_name + ' Top Cited Authors in his/her top ' + str(x_most_rel) + ' papers'])
    headers = ['Author Name', 'Total Citation Count']
    writer.writerow(headers)

    cited_authors = cross_cite_dict['Author_citation_frequency']
    for author in cited_authors:
        name = author[1].title() + ' ' + author[2].title()
        count = author[3]
        writer.writerow([name, count])

    writer.writerow(['\n'])
    writer.writerow(['Cross Cite Count to ' + orig_name + ' in the authors\' top papers\n'])
    

    cross_cite_arr = cross_cite_dict['Cited_authors_overcite_frequency']
    for author in cross_cite_arr:
        name = author[1].title() + ' ' + author[2].title()
        pap_an = 'Papers Analyzed: ' + str(author[4] - len([p for p in author[3] if p[1]==-1]))
        writer.writerow([name, pap_an])

        headers2 = ['Paper Name', 'Total Cross Citation Count']
        writer.writerow(headers2)

        total_cites = 0
        for paper_info in author[3]:
            if paper_info[1] == -1:
                writer.writerow([paper_info[0], 'No PDF'])
            else:
                writer.writerow([paper_info[0], paper_info[1]])

            if paper_info[1] != -1:
                total_cites += paper_info[1]

        writer.writerow(['Total Citations:',total_cites])
        writer.writerow('\n')



# j = [['Range-free localization schemes for large scale sensor networks', {'Journal Of Combinatorial Optimization': 1, 'Proceedings Of The 10Th Annual International  …': 1, '…  Of The 4Th International Symposium On  …': 1, 'Handbook Of Sensor Networks: Algorithms  …': 1, 'Proceedings Of The 4Th International Symposium  …': 1, 'Proceedings Of The 3Rd Acm Workshop On  …': 1, '…  Ieee 24Th Annual Joint Conference Of The  …': 1, '2004': 1, 'Computer  …': 1, 'Ieee Transactions  …': 1, 'Proceedings Of The 2Nd  …': 2, 'Ieee Transactions On Vehicular  …': 1, '…  Of The 1St International Conference On  …': 1, 'Ieee Signal Processing  …': 1, 'Proceedings Of The 13Th Annual Acm International  …': 1, 'Ndss': 1, '…  2004. Twenty-Third  …': 1, 'Proceedings Of The 3Rd International Symposium On  …': 1, 'Real-Time Systems  …': 1, '2007': 1, 'Ieee Transactions On Mobile  …': 1, 'Ieee Transactions On Wireless  …': 1, 'Proceedings Of The 10Th …': 1, 'Computer Networks': 1, 'Ieee Wireless  …': 1, 'Acm Transactions On  …': 2, '2005': 1, 'Ieee Journal On Selected Areas In  …': 1}]]
# jounal_dict_writer(j, 'data/abdelzaher/test')
