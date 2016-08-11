'''
Created on Jan 05, 2016

@author: Ankai
This file is used for random things I want to test out, for convenience
'''

import SessionInitializer
from urllib.request import Request, urlopen
from _io import BytesIO
import PyPDF2


sesh = SessionInitializer.getSesh()

url = 'http://dl.acm.org.proxy.lib.uwaterloo.ca/ft_gateway.cfm?id=2842628&ftid=1673282&dwn=1&CFID=654182719&CFTOKEN=18157975'
remoteFile = urlopen(Request(url)).read()
localFile = BytesIO(remoteFile)

pdf = PyPDF2.PdfFileReader(localFile)
print(pdf.getNumPages)