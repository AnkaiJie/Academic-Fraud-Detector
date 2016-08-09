
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

titles = []

with open("vas_top50_most_rel_overcites.csv", "r", encoding='latin1') as file:
    reader = csv.reader(file)
    for idx,line in enumerate(reader):
        if idx>0:
            t=[line[1].strip(),line[2]]
            if t[0] != 'Paper Title' and t[0] != 'Total' and t[1].isdigit():
                titles.append([t[0], int(t[1])])

titles = [t for t in titles if t[1] >=15]
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


# 134 papers over 15 cites, but only 21 unique ones. 
# These 21 papers cite vasilakos 456 times in total - average 21 papers
final = {'journals': {'Wireless  …': 1, 'Wireless Networks': 19, 'Proceedings of the ACM/IEEE  …': 1}, 'publishers': {'Springer': 20, 'dl.acm.org': 1}, 'authors': {' R Misra': 1, 'RH Jhaveri': 1, ' JY Song': 1, 'PK Batra': 1, ' N Panwar': 2, ' NM Patel': 1, ' M Chen': 1, ' H Al-Wattar': 1, ' JY Zou': 1, ' AWA Wahab…': 1, ' W Deng': 1, ' YC Chang': 1, 'S Dolev': 2, ' B Shah': 1, ' I Keshtkar': 1, ' DQ Wang': 1, ' RC Jin': 1, ' MY Alias': 1, ' Y Fanaeian': 1, ' MYI Idris': 1, 'M Ghiyasvand': 1, ' Z Zhang': 1, ' Y Liu': 1, ' OG Hafif': 1, ' L Zeng': 1, 'AE Kostin': 1, 'JMY Lim': 1, ' JH Ding': 1, ' A Kannan': 1, 'SK Bhoi': 2, 'Z Li': 1, 'Z Liu': 1, ' A Raj': 1, 'İ Abasıkeleş-Turgut': 1, ' K Kant': 1, ' M Abdullah': 1, 'MH Anisi': 1, ' WY Shin': 1, 'C Jeong': 1, ' KI Kim': 1, ' Ł Krzywiecki': 2, ' A Faruque': 1, 'K Vatanparvar': 1, 'CJ Lee': 1, 'Q Han': 1, ' J Wang': 1, ' J Loo': 1, 'R Logambigai': 1, 'T Gao': 1, ' G Zhang': 1, ' G Abdul-Salaam': 1, ' M Segal': 2, 'SA Alghamdi': 1, ' X He': 1, ' L Ye': 1, 'D Das': 1, ' PM Khilar': 2}}



