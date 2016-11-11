from selenium import webdriver
import selenium
import SessionInitializer
import shutil
from bs4 import BeautifulSoup
from urllib.request import urlopen

class WatLibParser:
    def __init__(self):
        self.ch = webdriver.Chrome("./chromedriver.exe")
        self.ch.get('https://www-scopus-com.proxy.lib.uwaterloo.ca/')

    def reset(self):
        self.ch = webdriver.Chrome("./chromedriver.exe")
        self.ch.get('https://www-scopus-com.proxy.lib.uwaterloo.ca/')

    def downloadPdfLink(self, link, path, source):
        print(link)
        session = SessionInitializer.getSesh()
        r = session.get(link, stream=True)

        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            return 1

        print('Error: ' + source + ' pdf was not downloaded correctly.')
        return None

    def downloadScholarPortal(self, href, path):
        href.click()
        try:
            pdfxmlTag = self.ch.find_element_by_xpath("//div[@class='download-btn']/a[text()='PDF Download']")
            pdfxmllink = pdfxmlTag.get_attribute('href')
        except selenium.common.exceptions.NoSuchElementException:
            print('Racer or invalid link only, no scholarsportal returning none...')
            return None

        return self.downloadPdfLink(pdfxmllink, path, 'Scholars Portal')

    def downloadSpringerOpen(self, path):
        try:
            pdfTag = self.ch.find_element_by_xpath("//p[@class='SideBox_action']/a[text()='Download PDF']")
            pdfLink = pdfTag.get_attribute('href')
            p1idx = pdfLink.find(';jwcn')
            pdfLink = pdfLink[p1idx+1:] + pdfLink[:p1idx + 1]
            extidx = pdfLink.find('?site=')
            if (extidx!=-1):
                pdfLink = pdfLink[:extidx]

        except selenium.common.exceptions.NoSuchElementException:
            print('Springer open link has no PDF, return trying v2...')
            try:
                pdfTag = self.ch.find_element_by_xpath("//p[@class='u-marginBtmM']/a[text()='Download PDF']")
                pdfLink = pdfTag.get_attribute('href')
            except selenium.common.exceptions.NoSuchElementException:
                print('Springer open link has no PDF, trying V2...')
                return None

        return self.downloadPdfLink(pdfLink, path, 'Springer Open')

    def downloadMdpi(self, path):
        try:
            pdfTag = self.ch.find_element_by_xpath("//li/a[text()='Full-Text PDF']")
            pdfLink = pdfTag.get_attribute('href')
        except selenium.common.exceptions.NoSuchElementException:
            print('MDPI link has no PDF, returning None...')
            return None

        return self.downloadPdfLink(pdfLink, path, 'MDPI')

    #REJECTS CRAWLER SOFTWARE CAN'T DO ANYTHING
    # def downloadScienceDirect(self, path):
    #     try:
    #         pdfTag = self.ch.find_element_by_xpath("//a[@title='Download PDF']")
    #         pdfLink = pdfTag.get_attribute('href')
    #     except selenium.common.exceptions.NoSuchElementException:
    #         print('ScienceDirect link has no PDF, returning None...')
    #         return None

    #     return self.downloadPdfLink(pdfLink, path, 'ScienceDirect')


    def downloadDOAJ(self, href, path):
        href.click()
        if 'springeropen' in self.ch.current_url:
            return self.downloadSpringerOpen(path)
        elif 'mdpi.com' in self.ch.current_url:
            return self.downloadMdpi(path)
        return None

    def downloadSpringerLinkCurrent(self, href, path):
        href.click()
        try:
            pdfTag = self.ch.find_element_by_xpath("//a[@title='Download this article in PDF format']")
            pdfLink = pdfTag.get_attribute('href')
        except selenium.common.exceptions.NoSuchElementException:
            print('springer current no tag download issue')
            return None

        return self.downloadPdfLink(pdfLink, path, 'SpringerLinkCurrent')


    def downloadIEEE(self, href, path):
        href.click()
        session = SessionInitializer.getSesh()
        resp = session.get(self.ch.current_url)
        src = BeautifulSoup(resp.content, 'lxml').text

        idx = src.find('"pdfUrl"')
        src = src[idx:]
        idx = src.find(':')
        idx2 = src.find(',')
        src = src[idx+1:idx2].strip().strip('"')
        url = 'http://ieeexplore.ieee.org.proxy.lib.uwaterloo.ca' + src
        print(url)
        resp2 = session.get(url)
        wrapperPage = BeautifulSoup(resp2.content, 'lxml')
        frames = wrapperPage.findAll('frame')
        srcFrame = None
        for frame in frames:
            if frame['src'] and 'http' in frame['src']:
                srcFrame = frame['src']

        if srcFrame:
            return self.downloadPdfLink(srcFrame, path, 'IEEE')
        else:
            return None


    def downloadFromWatLib(self, url, path, linkNo=1):
        self.ch.get(url)

        # Multi object waterloo page comes up sometimes - just go to the first one
        if 'multi.cgi?' in self.ch.current_url:
            link1 = self.ch.find_element_by_xpath("//h2[@class='exlHeadingTextDisplay']/a").get_attribute('href')
            self.ch.get(link1)

        source = ''

        try:
            #href = ch.find_element_by_link_text('Scholars Portal')
            #href = ch.find_element_by_xpath('//a[@href="javascript:openWindow(this, \'basic1\');" and text()="Scholars Portal"]')
            href = self.ch.find_element_by_xpath('//a[@href="javascript:openWindow(this, \'basic' + str(linkNo) + '\');"]')
            source = href.text
        except selenium.common.exceptions.NoSuchElementException:
            print('cannot find any link on webpage')
            return None
        except Exception as e:
            print('Couldn\'t find any text in source ' + str(e))
            return None

        result = None
        if source == 'Scholars Portal':
            result = self.downloadScholarPortal(href, path)
        elif source == 'DOAJ Directory of Open Access Journals':
            result = self.downloadDOAJ(href, path)
        elif 'SpringerLink' in source:
            result = self.downloadSpringerLinkCurrent(href, path)
        elif 'ieee' in source.lower():
            result = self.downloadIEEE(href, path)

        if not result:
            return self.downloadFromWatLib(url, path, linkNo=2)
        else:
            return result

        
    def goto(self, url):
        self.ch.get(url)


url = 'http://sfx.scholarsportal.info.proxy.lib.uwaterloo.ca/waterloo?sid=Elsevier:Scopus&_service_type=getFullTxt&issn=15253511&isbn=9781467398145&volume=2016-September&issue=&spage=&epage=&pages=&artnum=7564733&date=2016&id=doi:10.1109%2fWCNC.2016.7564733&title=IEEE+Wireless+Communications+and+Networking+Conference%2c+WCNC&atitle=Parameter+estimation+of+inverse+Gaussian+channel+for+diffusion-based+molecular+communication&aufirst=L.&auinit=L.&auinit1=L&aulast=Lin'
wl = WatLibParser()
wl.downloadFromWatLib(url, 'paper.pdf')

# s = SessionInitializer.getSesh()
# r = s.get('http://ieeexplore.ieee.org.proxy.lib.uwaterloo.ca/stamp/stamp.jsp?arnumber=7564733')
# soup = BeautifulSoup(r.content, 'lxml')
# print(soup)

# session = SessionInitializer.getSesh()
# resp2 = session.get('http://ieeexplore.ieee.org.proxy.lib.uwaterloo.ca/stamp/stamp.jsp?tp=&arnumber=7564733')
# wrapperPage = BeautifulSoup(resp2.content, 'lxml')
# frames = wrapperPage.findAll('frame')
# srcFrame = None
# for frame in frames:
#     if frame['src'] and 'http' in frame['src']:
#         srcFrame = frame['src']

# print(srcFrame)