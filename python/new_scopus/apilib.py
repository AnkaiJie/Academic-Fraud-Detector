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

    # returns basic info about a given author
    def getAuthorMetrics(self, auth_id):
        url = "http://api.elsevier.com/content/author?author_id=" + str(auth_id) + "&view=metrics"
        return self.reqs.getJson(url)

    #returns array of author papers
    def getAuthorPapers(self, auth_id, start=0, num=100):
        url = "http://api.elsevier.com/content/search/scopus?query=AU-ID(" + str(auth_id) + ")&field=eid,identifier,pubyear,title&sort=citedby-count&count=100"
        if start is not 0:
            url += "&start=" + str(start) + "&num=" + str(num)
        results = self.reqs.getJson(url)
        return results#['search-results']["entry"]

    # returns an array of papers that cite the paper with the given eid    
    def getCitingPapers(self, eid):
        #eid = '2-s2.0-79956094375'
        url ='https://api.elsevier.com/content/search/scopus?query=refeid(' + str(eid) + ')'
        return self.reqs.getJson(url)['search-results']['entry']

    #returns basic info about a paper with the given eid
    def getPaperInfo(self, eid):
        url = 'https://api.elsevier.com/content/abstract/eid/' + str(eid) + '?&field=authors,title,pubdatetxt,publicationName'
        return self.reqs.getJson(url)

    # returns an array of papers that the paper with the given eid cites
    def getPaperReferences(self, eid):
        url = 'https://api.elsevier.com/content/abstract/eid/' + str(eid) + '?&view=REF'
        return self.reqs.getJson(url)['abstracts-retrieval-response']['references']['reference']

    #makes a jsonObj pretty
    def prettifyJson(self, jsonObj):
        return self.reqs.prettifyJson(jsonObj)


# all the SQL code to insert/update is here
class DbInterface:
    def __init_(self):
        #definition of DB tables should be initialized here
        return

    #enters a citation record into database
    def pushCitation(record_dict):
        
        return

    #enters an author record into database
    def pushAuthor(record_dict):
        return

    #enters a paper record, and the necessary number of author-paper records into the database
    def pushPaper(record_dict):
        return


# all the API return value parsing should be placed here
# there is no sql code in this class, that should all be handled in DbInterface()
class ApiToDB:
    def __init__(self):
        self.dbi = DbInterface()
        self.sApi = ScopusApiLib()
        return

    # this should be the only method that the client interacts with
    def storeAuthorMain(self, auth_id, start_index=0, pap_num=100):
        # Puts the main author record
        # Puts the authors papers
        # Puts the citing papers of the authors papers, and those respective authors
        # Puts the cited papers of the authors papers, and those respective authors
        return

    # given author id, puts only an author record in db
    def storeAuthorOnly(self, auth_id):
        return

    # given author id and paper eid, stores the paper in db, as well as author-paper relation
    def storePaperOnly(self, auth_id, eid):
        return

    # given the src/targ eids, src/targ auth_ids, stores the citation relation into db
    def storeCitation(self, src_authid, src_eid, targ_authid, targ_eid):
        return



sal = ScopusApiLib()
# print(getAuthorMetrics('22954842600'))
# k = sal.getAuthorPapers(22954842600)
# print(sal.getCitingPapers('2-s2.0-79956094375'))
# k = sal.getPaperReferences('2-s2.0-79956094375')
#k = sal.getPaperInfo('2-s2.0-79956094375')
print(sal.prettifyJson(k))
