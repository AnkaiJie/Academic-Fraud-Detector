from credentials import API_KEY
import requests
import json


class reqWrapper:
    def __init__(self, headers):
         self.sesh = requests.session()
         self.headers = headers

    def get(self, url):
        return self.sesh.get(url, headers=self.headers)

    def getJson(self, url):
        return self.sesh.get(url, headers=self.headers).json()

    def getJsonPretty(self, url):
        resp = self.sesh.get(url, headers=self.headers)
        return json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': '))

    def prettifyJson(self, jsonObj):
        return json.dumps(jsonObj, sort_keys=True, indent=4, separators=(',', ': '))


class ScopusApiLib:

    def __init__(self):
        headers={'Accept':'application/json', 'X-ELS-APIKey': API_KEY}
        self.reqs = reqWrapper(headers)

    def getAuthorMetrics(self, auth_id):
        url = "http://api.elsevier.com/content/author?author_id=" + str(auth_id) + "&view=metrics"
        return self.reqs.getJsonPretty(url)


    def getAuthorPapers(self, auth_id):
        url = "http://api.elsevier.com/content/search/scopus?query=AU-ID(" + str(auth_id) + ")&field=eid,identifier,title&sort=citedby-count&count=10"
        results = self.reqs.getJson(url)
        return results['search-results']["entry"]

    def getCitingPapers(self, eid):
        #eid = '2-s2.0-79956094375'
        url ='https://api.elsevier.com/content/search/scopus?query=refeid(' + str(eid) + ')'
        return self.reqs.getJsonPretty(url)['search-results']['entry']

    def getPaperReferences(self, eid):
        url = 'https://api.elsevier.com/content/abstract/EID:' + str(eid) + '?&view=REF'
        return self.reqs.getJsonPretty(url)['abstracts-retrieval-response']


class 


sal = ScopusApiLib()
# print(getAuthorMetrics(22954842600))
# print(getAuthorPapers())
# print(sal.getCitingPapers('2-s2.0-79956094375'))
print (sal.getPaperReferences('2-s2.0-79956094375'))
