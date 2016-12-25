from credentials import API_KEY, DBNAME, USER, PASSWORD, HOST
import requests
import json
import sys
import pymysql

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
        keys = list(profile.keys())
        for k in keys:
            if 'preferred-name' in k:
                profile[k.split('_')[1]] = profile.pop(k)
        if 'given-name' in profile and profile['given-name'] is not None:
            profile['given-name'] = self.processFirstName(profile['given-name'])
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
    def getCitingPapers(self, eid, num=100):
        #eid = '2-s2.0-79956094375'
        url ='https://api.elsevier.com/content/search/scopus?query=refeid(' + str(eid) + ')&field=eid,title&start=0&count=' + str(num)
        resp = self.reqs.getJson(url)['search-results']['entry']
        return [pap['eid'] for pap in resp]

    #returns basic info about a paper with the given eid
    def getPaperInfo(self, eid):
        url = 'https://api.elsevier.com/content/abstract/eid/' + str(eid) + '?&field=authors,coverDate,eid,title,publicationName'
        resp = self.reqs.getJson(url)
        try:
            resp = resp['abstracts-retrieval-response']
        except:
            print(resp)
            raise
        coredata = resp['coredata']
        if resp['authors']:
            authors = resp['authors']['author']
            auinfos = self.processAuthorList(authors)
            coredata['authors'] = auinfos
        coredata = self.utility.removePrefix(coredata)
        return coredata

    def processFirstName(self, name):
        return name.split()[0]

    def processAuthorList(self, arr):
        auids = []
        for a in arr:
            if '@auid' in a and a['@auid'] != '':
                res = self.utility.filter(a, ['@auid', 'ce:indexed-name', 'ce:initials', 'ce:surname', 'ce:given-name'])
                res = self.utility.removePrefix(res)
                self.utility.replaceKey(res, '@auid', 'dc:identifier')
                res['dc:identifier'] = 'AUTHOR_ID:' + res['dc:identifier']
                auids.append(res)
            else: 
                #no scopus id, just use name as id
                res = self.utility.filter(a, ['ce:indexed-name', 'ce:initials', 'ce:surname', 'ce:given-name'])
                res = self.utility.removePrefix(res)

                newid = 'AUTHOR_ID:'
                id_arr = []
                if 'initials' in res:
                    id_arr.append(res['initials'])
                if 'surname' in res:
                    id_arr.append(res['surname'])

                newid += '_'.join(id_arr)
                res['dc:identifier'] = newid

                auids.append(res)
        return auids

    # returns an array of papers that the paper with the given eid cites
    def getPaperReferences(self, eid, refCount = -1):
        url = 'https://api.elsevier.com/content/abstract/eid/' + str(eid) + '?&view=REF'
        if refCount is not -1:
            url += '&refcount=' + str(refCount)
        
        resp = self.reqs.getJson(url)
        resp_body = resp['abstracts-retrieval-response']
        if resp_body is None:
            return None
        else:
            resp_body = resp_body['references']['reference']

        ref_arr = []
        for raw in resp_body:
            ref_dict = {}
            ref_dict['authors'] = None
            if raw['author-list'] and raw['author-list']['author']:
                auth_list = raw['author-list']['author']
                auids = self.processAuthorList(auth_list)
                ref_dict['authors'] = auids

            ref_dict['srceid'] = eid
            ref_dict['eid'] = raw['scopus-eid']
            ref_arr.append(ref_dict)

        return ref_arr

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

    def removePrefix (self, origDict, sep=':'):
        d = dict(origDict)
        rem = []
        for key, value in d.items():
            if len(key.split(sep)) > 1:
                rem.append(key)
        for k in rem:
            newkey = k.split(sep)[1]
            d[newkey] = d.pop(k)
        return d

    def addPrefixToKeys(self, dOrig, prefix):
        d = dict(dOrig)
        keys = list(d.keys())
        for key in keys:
            d[prefix+key] = d.pop(key) 
        return d

    #stack overflow code
    def merge_dicts(self, *dict_args):
        '''
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        '''
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return dict(result)

    def changeKeyString(self, d, change, toThis):
        keys = list(d.keys())
        for key in keys:
            newKey = key.replace(change, toThis)
            d[newKey] = d.pop(key)

    def changeValueString(self, d, change, toThis):
        for key, val in d.items():
            if change in val:
                d[key] = val.replace(change, toThis)

    def replaceKey(self, d, change, toThis):
        d[toThis] = d.pop(change)

    def removeNone(self, d):
        keys = list(d.keys())
        for key in keys:
            if d[key] is None:
                d.pop(key)

# all the SQL code to insert/update is here
class DbInterface:
    def __init__(self):
        self.utility = Utility()
        self.scops = ScopusApiLib()
        #self.sql = 

    def pushToS1(self, srcPaperDict, targPaperDict, srcAuthor, targAuthor):

        srcPaperDict = self.utility.addPrefixToKeys(srcPaperDict, 'src_paper_')
        targPaperDict = self.utility.addPrefixToKeys(targPaperDict, 'targ_paper_')
        srcAuthor = self.utility.addPrefixToKeys(srcAuthor, 'src_author_')
        targAuthor = self.utility.addPrefixToKeys(targAuthor, 'targ_author_')

        aggDict = self.utility.merge_dicts(srcPaperDict, targPaperDict, srcAuthor, targAuthor)
        self.utility.removeNone(aggDict)
        self.utility.changeKeyString(aggDict, '-', '_')
        self.utility.changeKeyString(aggDict, '@', '')
        self.utility.changeKeyString(aggDict, ':', '_')
        self.utility.changeValueString(aggDict, '"', '\\"')

        print(self.toString(aggDict))
        self.pushDict('citations_s1', aggDict)

    def toString(self, aggDict):
        srcp = None
        targp = None
        srca = None
        targa = None
        if 'src_paper_title' in aggDict:
            srcp = aggDict['src_paper_title']
        if 'targ_paper_title' in aggDict:
            targp = aggDict['targ_paper_title']
        if 'src_author_indexed_name' in aggDict:
            srca = aggDict['src_author_indexed_name']
        if 'targ_author_indexed_name' in aggDict:
            targa = aggDict['targ_author_indexed_name']
        return 'Source: ' + str(srca) + ' / ' + str(srcp) + ' ------------- ' + 'Target: ' + str(targa) + ' / ' + str(targp)

    def pushDict(self, table, d):
        conn = pymysql.connect(HOST, USER, PASSWORD, DBNAME, charset='utf8')
        cur = conn.cursor()

        keys = d.keys()
        vals = d.values()
        vals = ['"' + v + '"' for v in vals if v is not None]
        command = "REPLACE INTO %s (%s) VALUES(%s)" % (
            table, ",".join(keys), ",".join(vals))
        try:
            cur.execute(command)
        except:
            print(command)
            raise
        conn.commit()
        cur.close()
        conn.close()


# all the API return value parsing should be placed here
# any text/key processing is done here
# there is no sql code in this class, that should all be handled in DbInterface()
class ApiToDB:
    def __init__(self):
        self.dbi = DbInterface()
        self.sApi = ScopusApiLib()
        self.utility = Utility()

    # this should be the only method that the client interacts with
    def storeAuthorMain(self, auth_id, start_index=0, pap_num=100, cite_num=100, refCount=-1):
        # Puts the main author record
        print('Running script on author: ' + str(auth_id))
        
        # Puts the authors papers
        print('Getting author papers')
        papers = self.sApi.getAuthorPapers(auth_id, start=start_index, num=pap_num)
        for eid in papers:
            print('Beginning processing for paper: ' + eid)
            #main_title = self.storePapersOnly(eid)
            references = self.sApi.getPaperReferences(eid, refCount=refCount)
            if references is None:
                print('No Data on References')
                references = []
            citedbys = self.sApi.getCitingPapers(eid, num=cite_num)

            #Puts the citing papers of the authors papers, and those respective authors
            print('Handling citing papers...')
            for citing in citedbys:
                self.storeToStage1(citing, eid)
                self.storePaperReferences(citing, refCount=refCount)
            print('Done citing papers.')

            # Puts the cited papers of the authors papers, and those respective authors
            print('Handling references...')
            #Repeated code from storePaperReferences for clarity
            for ref in references:
                refid = ref['eid']
                self.storeToStage1(eid, refid)
                self.storePaperReferences(refid, refCount=refCount)
            print('Done references')

    def storePaperReferences(self, eid, refCount=-1):
        references = self.sApi.getPaperReferences(eid, refCount=refCount)
        for ref in references:
            refid = ref['eid']
            self.storeToStage1(eid, refid)


    def storeToStage1(self, srcpapid, targpapid):
        srcPaperDict = self.sApi.getPaperInfo(srcpapid)
        targPaperDict = self.sApi.getPaperInfo(targpapid)
        srcAuthors = [{'indexed_name': None}]
        targAuthors = [{'indexed_name': None}]
        if 'authors' in srcPaperDict:
            srcAuthors = srcPaperDict.pop('authors')
        if 'authors' in targPaperDict:
            targAuthors = targPaperDict.pop('authors')

        for srcAuth in srcAuthors:
            for targAuth in targAuthors:
                self.dbi.pushToS1(srcPaperDict, targPaperDict, srcAuth, targAuth)

    def getAuthorsFromPaper(self, origPaperDict):
        paperDict = dict(origPaperDict)

        author_arr = []
        if 'authors' in paperDict:
            for authid in paperDict['authors']:
                if isinstance(authid, dict):
                    author_arr.append(authid)
                else:
                    author_info = self.getAuthorInfo(authid)
                    author_arr.append(author_info)
            origPaperDict.pop('authors')
        return author_arr

    def getAuthorInfo(self, auth_id):
        author = self.sApi.getAuthorMetrics(auth_id)
        return author




