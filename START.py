from academicThings import AcademicPublisher
from _csv import Error
import traceback
from csvWriter import *
from scrapper import count_cross_cites, count_overcites, count_self_cites, count_journal_frequency


print('Academic Fraud Detector')
authorlink = input('Please enter the Google Scholar profile link of the author you want to investigate:\n')
entered_author = AcademicPublisher(authorlink, 1)

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