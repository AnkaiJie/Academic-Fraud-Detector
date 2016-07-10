'''
Created on Jan 05, 2016

@author: Ankai
This file is used for random things I want to test out, for convenience
'''
from lxml import etree
import offCampusLogin
import urllib.request as ur
import shutil
from _io import BytesIO
import PyPDF2
import sys
from io import TextIOWrapper
from bs4 import BeautifulSoup
from ReferenceParser import PdfObj
#sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# session = offCampusLogin.getSesh()
# r = session.get('http://journals1.scholarsportal.info.proxy.lib.uwaterloo.ca/pdf/21682194/v17i0003/579_asoaltfoa.xml', stream=True)

# if r.status_code == 200:
#     with open('ankai.pdf', 'wb') as f:
#         r.raw.decode_content = True
#         shutil.copyfileobj(r.raw, f)

# def getPDFContent(path):
#     content = ""
#     p = open(path, "rb")
#     pdf = PyPDF2.PdfFileReader(p)
#     num_pages = pdf.getNumPages()
#     for i in range(0, num_pages):
#         content += pdf.getPage(i).extractText()
#     return content 

# content = getPDFContent('ankai.pdf')

# print(content)

# root = etree.fromstring(response.text)
# print(root)pankai

# response = session.get('https://scholar-google-ca.proxy.lib.uwaterloo.ca/scholar?start=10&hl=en&as_sdt=0,5&sciodt=0,5&cites=13991517909897415820&scipsc=')
# soup = BeautifulSoup(response.content, 'lxml')
# linkExtracts = soup.findAll('div', attrs={'class': 'gs_md_wp gs_ttss'})
# pdfList = []

# for extract in linkExtracts:
#     #this code will skip links with [HTML] tag and throw error for links that are only "Get it at UWaterloo"
#     tag = extract.find('span', attrs={'class': 'gs_ctg2'})
#     if tag is not None and tag.text == "[PDF]":
#         pdf = PdfObj('url', extract.find('a')['href'])
#         pdfList.append(pdf)
#     elif tag is not None:
#         print('Non-PDF tag, using get it @ waterloo')

#     potential_links = extract.findAll('a')
#     for link in potential_links:
#         if link.text.strip() == "Get It!@Waterloo":
#             pdfList.append(link['href'])
# print (pdfList[1])

# response = session.get(pdfList[1])
# soup = BeautifulSoup(response.content, 'lxml')
# script = soup.find('script').text
# replace_link = script[18:-2]

# response = session.get(replace_link)
# fuck i need selenium
# response = session.get('http://sfx.scholarsportal.info.proxy.lib.uwaterloo.ca/waterloo/cgi/core/sfxresolver.cgi?tmp_ctx_svc_id=1&tmp_ctx_obj_id=1&service_id=13760000000000146&request_id=11525252')
# print(response.text)

#print(response.text)
#soup = BeautifulSoup(response.content, 'lxml')

