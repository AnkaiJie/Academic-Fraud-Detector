'''
Created on Jan 17, 2016

@author: Ankai
'''
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from urllib.request import Request
import requests
import lxml 


class Paper:
    def __init__ (self, link):
        self.__url = link
        self.__pap_info = {}
        
        session = requests.session()
        response = session.get(self.__url)
        
        soup = BeautifulSoup(response.content, 'lxml')

        self.__pap_info['Title'] = soup.find('a', attrs={'class': 'gsc_title_link'}).text
        
        div_info_table = soup.find('div', attrs={'id':'gsc_table'})
        div_fields = div_info_table.find_all('div', attrs={'class':'gs_scl'})
        
        for field in div_fields:
            fieldName = field.find('div', attrs={'class':'gsc_field'}).text
            if (fieldName=="Description"):
                break
            self.__pap_info[fieldName] = field.find('div', attrs={'class':'gsc_value'}).text
        
    def getUrl(self):
        return self.__url
        
    def getInfo (self):
        return self.__pap_info
        
        
class AcademicPublisher:

    def __init__ (self, name, mainUrl):
        
        self.name = name
        self.url = mainUrl        
        '''self.url = self.url + '&cstart=0&pagesize=' + str(numResults)
        values = {'s':'basics',
                  'submit':'search'}
        data = urllib.parse.urlencode(values)
        self.data = data.encode(encoding='utf-8')
        req = urllib.request.Request(self.url, self.data)
        resp = urllib.request.urlopen(req)
        self.respData = resp.read()
        #print(self.respData)
        print(self.getWorksListOnPage(self.respData))'''
    
    def getPapers(self, numResults):
        session = requests.Session()
        response = session.get(self.url + '&cstart=0&pagesize=' + str(numResults))
        
        soup = BeautifulSoup(response.content, "lxml")
        
        paper_list = []
        for one_url in soup.findAll('a', attrs={'class':'gsc_a_at'}, href=True):
            paper_list.append(Paper('https://scholar.google.ca' + one_url['href']))
            
    
            
        return paper_list
        
        
