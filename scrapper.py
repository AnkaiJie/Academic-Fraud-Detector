'''
Created on Jan 7, 2016

@author: Ankai
'''
import urllib.request
import urllib.parse
import re
import site
from bs4 import BeautifulSoup
from urllib.request import Request
import requests
import html5lib
import lxml 

class AcademicPublisher:

    def __init__ (self, name, mainUrl):
        
        self.name = name
        self.url = mainUrl
        
    
    def getWorksListOnPage(self, loadedResponse):
        soup = BeautifulSoup(loadedResponse, "html5lib", from_encoding='ISO-8859-1')
        
        print(soup)
        self.worksList = []
        
        worksTable = soup.find('tbody', attrs={'id': 'gsc_a_b'})
        
        for row in worksTable.findAll('tr'):
            title = row.find('td', attrs={'class':'gsc_a_t'}).find('a', attrs={'class':'gsc_a_at'}).text
            authors = row.find('td', attrs={'class':'gsc_a_t'}).find('div', attrs={'class':'gs_gray'}).text
            numCited = row.find('td', attrs={'class':'gsc_a_c'}).find('a', attrs={'class':'gsc_a_ac'}).text
            tempDict = {'title':title, 'authors': authors, 'numCiters': numCited}
            self.worksList.append(tempDict)
            
        return self.worksList
    
    def loadWorksList(self, numResults):
        session = requests.Session()
        
        params = {}
        response = session.get('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao&cstart=0&pagesize=78')
        print(response.content)
        print(self.getWorksListOnPage(response.content))
         
        
        '''self.url = 'https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao&cstart=0&pagesize=78'
        values = {'s':'basics',
                  'submit':'search'}
        data = urllib.parse.urlencode(values)
        self.data = data.encode(encoding='ISO-8859-1', errors='strict')
        req = urllib.request.Request(self.url, self.data)
        resp = urllib.request.urlopen(req)
        self.respData = resp.read()
        print(self.getWorksListOnPage(self.respData))'''
        

    
vasilakos = AcademicPublisher('Anthoninos Vasilakos', 'https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao')

vasilakos.loadWorksList(300)
