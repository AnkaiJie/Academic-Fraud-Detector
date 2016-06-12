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
sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# session = offCampusLogin.getSesh()
# r = session.get('http://journals1.scholarsportal.info.proxy.lib.uwaterloo.ca/pdf/21682194/v17i0003/579_asoaltfoa.xml', stream=True)

# if r.status_code == 200:
#     with open('ankai.pdf', 'wb') as f:
#         r.raw.decode_content = True
#         shutil.copyfileobj(r.raw, f)

def getPDFContent(path):
    content = ""
    p = open(path, "rb")
    pdf = PyPDF2.PdfFileReader(p)
    num_pages = pdf.getNumPages()
    for i in range(0, num_pages):
        content += pdf.getPage(i).extractText()
    return content 



content = getPDFContent('ankai.pdf')

print(content)

# root = etree.fromstring(response.text)
# print(root)pankai