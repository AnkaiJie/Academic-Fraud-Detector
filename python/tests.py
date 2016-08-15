'''
Created on Jan 05, 2016

@author: Ankai
This file is used for random things I want to test out, for convenience
'''

from ReferenceParser import PaperReferenceExtractor, PdfObj

pre = PaperReferenceExtractor()
p = PdfObj('local', 'paper.pdf')
print(pre.getReferencesContent(p))
print(pre.getCitesToAuthor('Vasilakos', pre.getReferencesContent(p)))