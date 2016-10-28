# import PyPDF2


# p = open('paper2.pdf', "rb")
# pdf = PyPDF2.PdfFileReader(p)
# num_pages = pdf.getNumPages()
# pcont=''
# print(num_pages)
# for i in range(0, num_pages):
#   print('here')
#   pcont += pdf.getPage(i).extractText()

# print(pcont)

# print(pcont[0:300])
# from io import BytesIO
# from pdfminer.pdfinterp import PDFResourceManager, process_pdf
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams

# def to_txt(pdf_path):
#     input_ = open(pdf_path, 'rb')
#     output = BytesIO()

#     manager = PDFResourceManager()
#     converter = TextConverter(manager, output, laparams=LAParams())
#     process_pdf(manager, converter, input_)

#     return output.getvalue() 

# k = to_txt('paper2.pdf')
# print(k[0:10])

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

k=''

fp = open('paper.pdf', 'rb')
parser = PDFParser(fp)
doc = PDFDocument()
parser.set_document(doc)
doc.set_parser(parser)
doc.initialize('')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Process each page contained in the document.

k = 'lol'
print(k.find('ss'))