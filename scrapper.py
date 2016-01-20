'''
Created on Jan 7, 2016

@author: Ankai
'''

from AcademicThings import AcademicPublisher
from AcademicThings import GscPdfExtractor
 


somePerson = AcademicPublisher('Name', 'https://scholar.google.ca/citations?user=-EMkK7QAAAAJ&hl=en&oi=ao')

#(somePerson.getPapers(2)[0].getInfo())
#print(somePerson.getPaperCitationsByIndex(0))
print(GscPdfExtractor('https://scholar.google.ca/scholar?oi=bibs&hl=en&oe=ASCII&cites=13991517909897415820&as_sdt=5').findPaperUrls())
