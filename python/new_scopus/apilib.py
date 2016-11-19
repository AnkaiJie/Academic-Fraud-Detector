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

# this class returns flattened dictionaries of api keys
# it does some filtering and flattening of returned json, but doesn ot directly modify
class ScopusApiLib:

    def __init__(self):
        headers={'Accept':'application/json', 'X-ELS-APIKey': API_KEY}
        self.reqs = reqWrapper(headers)
        self.utility = Utility()

    # returns basic info about a given author
    def getAuthorMetrics(self, auth_id):
        url = "http://api.elsevier.com/content/author?author_id=" + str(auth_id)
        resp = self.reqs.getJson(url)['author-retrieval-response'][0]

        pfields = ['preferred-name', 'publication-range']
        cfields = ['citation-count', 'cited-by-count', 'dc:identifier', 'document-count', 'eid']
        profile = self.utility.filter(resp['author-profile'], pfields)
        coredata = self.utility.filter(resp['coredata'], cfields)
        profile.update(coredata)
        profile = self.utility.flattenDict(profile)
        return profile

    #returns array of author papers eids
    def getAuthorPapers(self, auth_id, start=0, num=100):
        auth_id = str(auth_id)
        if 'AUTHOR_ID' in auth_id:
            auth_id = auth_id.split(':')[1]

        url = "http://api.elsevier.com/content/search/scopus?query=AU-ID(" + auth_id + ")&field=eid&sort=citedby-count&start=" + \
            str(start) + "&count=" + str(num)
        if start is not 0:
            url += "&start=" + str(start) + "&num=" + str(num)
        results = self.reqs.getJson(url)['search-results']["entry"]
        eid_arr = []
        for pdict in results:
            eid_arr.append(pdict['eid'])
        return eid_arr

    # returns an array of papers that cite the paper with the given eid    
    def getCitingPapers(self, eid):
        #eid = '2-s2.0-79956094375'
        url ='https://api.elsevier.com/content/search/scopus?query=refeid(' + str(eid) + ')'
        return self.reqs.getJson(url)['search-results']['entry']

    #returns basic info about a paper with the given eid
    def getPaperInfo(self, eid):
        url = 'https://api.elsevier.com/content/abstract/eid/' + str(eid) + '?&field=authors,coverDate,eid,title,publicationName'
        return self.reqs.getJson(url)

    # returns an array of papers that the paper with the given eid cites
    def getPaperReferences(self, eid):
        url = 'https://api.elsevier.com/content/abstract/eid/' + str(eid) + '?&view=REF'
        return self.reqs.getJson(url)['abstracts-retrieval-response']['references']['reference']

    #makes a jsonObj pretty
    def prettifyJson(self, jsonObj):
        return self.reqs.prettifyJson(jsonObj)

class Utility:
    #returns dict with the wanted keys only, if keys empty, just flattens dict
    def flattenDict (self, d):
        def expand(key, value):
            if isinstance(value, dict):
                return [ (key + '_' + k, v) for k, v in self.flattenDict(value).items()]
            else:
                return [ (key, value) ]

        items = [ item for k, v in d.items() for item in expand(k, v) ]
        return dict(items)

    # if no keys specified, return original dictionary
    def filter(self, d, keys):
        if len(keys) is 0:
            return d
        dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
        return dictfilt(d, keys)


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
# any text/key processing is done here
# there is no sql code in this class, that should all be handled in DbInterface()
class ApiToDB:
    def __init__(self):
        self.dbi = DbInterface()
        self.sApi = ScopusApiLib()
        return

    # this should be the only method that the client interacts with
    def storeAuthorMain(self, auth_id, start_index=0, pap_num=100):
        # Puts the main author record
        author = self.sApi.getAuthorMetrics(auth_id)
        self.storeAuthorOnly(author)
        # Puts the authors papers
        papers = self.sApi.getAuthorPapers(author['dc:identifier'], 0, 100)
        for eid in papers:
            self.storePapersOnly(auth_id, eid)
        # Puts the citing papers of the authors papers, and those respective authors
        # Puts the cited papers of the authors papers, and those respective authors
        return

    # given author id, puts only an author record in db
    def storeAuthorOnly(self, auth_id):
        return

    # given author id and paper eid, stores the paper in db, as well as author-paper relation
    def storePapersOnly(self, auth_id, eid):
        return

    # given the src/targ eids, stores the citation relation into db
    def storeCitation(self, src_eid, targ_eid):
        return



sal = ScopusApiLib()
#k = sal.getAuthorMetrics(22954842600)
k = sal.getAuthorPapers("AUTHOR_ID:22954842600", 0, 2)
# print(sal.getCitingPapers('2-s2.0-79956094375'))
# k = sal.getPaperReferences('2-s2.0-79956094375')
#k = sal.getPaperInfo('2-s2.0-79956094375')
print(sal.prettifyJson(k))
