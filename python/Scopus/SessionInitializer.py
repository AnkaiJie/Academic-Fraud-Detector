import requests

#Internet Setup
session = requests.Session()
# Need an initialial get to prevent future redirect to home page
ROOT_URL = 'https://www-scopus-com.proxy.lib.uwaterloo.ca/'
session.get(ROOT_URL)


def getHeaders():
    return headers

def getSesh():
    return session
