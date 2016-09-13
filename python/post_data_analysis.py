
import csv
from collections import OrderedDict
import SessionInitializer
from bs4 import BeautifulSoup

def dedupe(seq):
    uniq = []
    for s in seq:
        if s not in uniq:
            uniq.append(s)
    return uniq

def add_freq_dict(d, el):
    if el in d:
        d[el] += 1
    else:
        d[el] = 1


def overcite_an(path):
    titles = []

    with open(path, "r", encoding='latin1') as file:
        reader = csv.reader(file)
        for idx,line in enumerate(reader):
            if idx>0:
                t=[line[1].strip(),line[2]]
                if t[0] != 'Paper Title' and t[0] != 'Total' and t[1].isdigit():
                    titles.append([t[0], int(t[1])])

    titles = [t for t in titles if t[1] >=25]
    print(len(titles))
    titles = dedupe(titles)
    print(len(titles))

    s = 0
    for t in titles:
        s += t[1]

    print(s)

    session = SessionInitializer.getSesh()
    headers = SessionInitializer.getHeaders()
    final_dict = {'authors': {}, 'journals': {}, 'publishers': {}}


    for t in titles:
        paper_name = t[0]
        paper_cites = t[1]
        query = "+".join(paper_name.split())

        url = SessionInitializer.ROOT_URL + '/scholar?q=' + query + '&btnG=&hl=en&as_sdt=0%2C5'
        print(url)
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        info_list = ""
        try:
            info_list = soup.find('div', attrs={'class' : 'gs_a'}).text
        except:
            print('cant find for ' + paper_name)
            continue
        info_list = [i.strip() for i in info_list.split(' - ')]

        authors = info_list[0].split(',')
        journal = info_list[1].split(',')[0]
        publisher = info_list[2]

        for a in authors:
            add_freq_dict(final_dict['authors'], a)

        add_freq_dict(final_dict['journals'], journal)
        add_freq_dict(final_dict['publishers'], publisher)
        print(publisher)
    print(final_dict)


def journal_an(path):
    titles = []
    tempsum = 0
    with open(path, "r", encoding='latin1') as file:
        reader = csv.reader(file)
        for idx,line in enumerate(reader):
            if idx>0 and len(line) > 1:
                t=[line[0].strip(),line[1]]
                if t[1].isdigit():
                    titles.append([t[0], int(t[1])])
                    tempsum+=int(t[1])
                

    print(tempsum)