'''
Created on Jan 7, 2016

@author: Ankai
'''

from academicThings import AcademicPublisher



vasilakos = AcademicPublisher('Anthoninos Vasilakos', 'https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao')

print (vasilakos.getPapers(2)[1].getInfo())
