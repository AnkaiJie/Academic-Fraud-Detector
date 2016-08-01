

import csv


'''
Created on Jan 05, 2016

@author: Ankai

NOTE: This CSV Writer was written for one specific author. It is hard-coded data for convenience
'''



def total_journal_dict_writer (totalJournalDict,name):
    writer = csv.writer(open(name+'.csv', 'w', encoding='utf-8'))
    for key, value in totalJournalDict.items():
        try:
            writer.writerow([key, value])
        except UnicodeEncodeError:
            continue


def jounal_dict_writer(indJournalArrays, name):
    writer = csv.writer(open(name + '.csv', 'w', encoding='utf-8'), lineterminator='\n')
    for paper in indJournalArrays:
        writer.writerow([paper[0]])
        for key, value in paper[1].items():
            try:
                writer.writerow([key, value])
            except UnicodeEncodeError:
                continue
        writer.writerow(['\n'])



def self_cite_writer(self_cite_arr, name):
    keys = self_cite_arr[0].keys()
    with open(name + '.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(self_cite_arr)



def over_cite_writer(over_cite_arr, name):

    writer = csv.writer(open(name + '.csv', 'w', encoding='utf-8'), lineterminator='\n')
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

    writer = csv.writer(open(name + '.csv', 'w', encoding='utf-8'), lineterminator='\n')

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
    writer.writerow(['Cross Cite Count to ' + orig_name + ' in the authors\' top papers'])
    headers2 = ['Author Name', 'Total Citation Count\t', 'Papers from IEEE or Springer Analyzed']
    writer.writerow(headers2)

    cross_cite_arr = cross_cite_dict['Cited_authors_overcite_frequency']
    for author in cross_cite_arr:
        name = author[1].title() + ' ' + author[2].title()
        count = author[3]
        y_most_rel = author[4]
        writer.writerow([name, count, y_most_rel])



# k = {'Cited_authors_overcite_frequency': [['<academicThings.AcademicPublisher object at 0x04836C90>', 'noam', 'nisan', 0, 0],
#  ['<academicThings.AcademicPublisher object at 0x04836030>', 'bo', 'an', 0, 0]], 
#  'First Name': 'athanasios', 'Last Name': 'vasilakos', 'y_most_rel': 0,
#   'Author_citation_frequency': [['<academicThings.AcademicPublisher object at 0x04836C90>', 'noam', 'nisan', 3],
#  ['<academicThings.AcademicPublisher object at 0x04836030>', 'bo', 'an', 2]], 'x_most_rel': 2}
# cross_cite_writer(k, 'cross_cite_test')