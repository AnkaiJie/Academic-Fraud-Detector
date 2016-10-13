import requests
from bs4 import BeautifulSoup

response = requests.get('https://www-scopus-com.proxy.lib.uwaterloo.ca/author/document/retrieval.uri?authorId=22954842600&tabSelected=docLi&sortType=cp-f&resultCount=2')
soup = BeautifulSoup(response.content, 'lxml')
print(soup)