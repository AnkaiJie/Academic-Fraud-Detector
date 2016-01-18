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


class AcademicPublisher:

    def __init__ (self, name, mainUrl):
        
        self.name = name
        self.url = mainUrl
        
    
    def getWorksListOnPage(self, loadedResponse):
        soup = BeautifulSoup(loadedResponse, "lxml")
        
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
        response = session.get(self.url + '&cstart=0&pagesize=' + str(numResults))
        
        print(self.getWorksListOnPage(response.content))
        
        
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
