import requests


# ROOT_URL = "https://scholar-google-ca.proxy.lib.uwaterloo.ca"
ROOT_URL = "https://scholar.google.ca"


#Internet Setup
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
#login_page = session.get('https://scholar-google-ca.proxy.lib.uwaterloo.ca/', headers=headers)
data = {'url':'https://scholar.google.ca/', 'pass': 'jie', 'user': '21187005749502'}
session.post('https://login.proxy.lib.uwaterloo.ca/login', data)
if ROOT_URL == "https://scholar-google-ca.proxy.lib.uwaterloo.ca":
    data = {'url':'https://scholar.google.ca/', 'pass': 'jie', 'user': '21187005749502'}
    session.post('https://login.proxy.lib.uwaterloo.ca/login', data)


def getHeaders():
    return headers

def getSesh():
    return session
