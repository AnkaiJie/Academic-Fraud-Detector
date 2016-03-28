'''
Created on Jan 05, 2016

@author: Ankai
'''
from bs4 import BeautifulSoup
import requests
import lxml
import re
import time


    
        
class AcademicPublisher:

    def loadPapers(self):
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}       
        response = session.get('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao&cstart=0&pagesize=15', headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        print(soup)
        arr=[]
    
        for one_url in soup.findAll('a', attrs={'class':'gsc_a_at'}, href=True):
            #one_url['href'] finds the link to the paper page
            arr.append('https://scholar.google.ca' + one_url['href'])
            print (one_url)
            # takes out all papers not from IEEE or Springer US 
            self.filterByPublishers()
            
            

k = AcademicPublisher()
k.loadPapers()