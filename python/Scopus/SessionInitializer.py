import requests

#Internet Setup
session = requests.Session()
# Need an initialial get to prevent future redirect to home page
session.get('https://www-scopus-com.proxy.lib.uwaterloo.ca/')


def getHeaders():
    return headers

def getSesh():
    return session
