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
        if 'given-name' in profile:
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
        resp = resp["abstracts-retrieval-response"]
        coredata = resp['coredata']
        if resp['authors']:
            authors = resp['authors']['author']
            auids = self.processAuthorList(authors)
            coredata['authors'] = auids
        coredata = self.utility.removePrefix(coredata)
        return coredata

    def processFirstName(self, name):
        return name.split()[0]

    def processAuthorList(self, arr):
        auids = []
        for a in arr:
            if '@auid' in a and a['@auid'] != '':
                auids.append(a['@auid'])
            else: 
                #no scopus id, just use name as id
                res = self.utility.filter(a, ['ce:indexed-name', 'ce:initials', 'ce:surname', 'ce:given-name'])
                res = self.utility.removePrefix(res)
                res['eid'] = res['initials'] + '_' + res['surname']
                auids.append(res)
        return auids

    # returns an array of papers that the paper with the given eid cites
    def getPaperReferences(self, eid, refCount = -1):
        url = 'https://api.elsevier.com/content/abstract/eid/' + str(eid) + '?&view=REF'
        if refCount is not -1:
            url += '&refcount=' + str(refCount)
        resp = self.reqs.getJson(url)['abstracts-retrieval-response']['references']['reference']
        ref_arr = []
        for raw in resp:
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
        self.utility.changeKeyString(aggDict, '-', '_')
        self.utility.changeKeyString(aggDict, '@', '')
        self.utility.changeKeyString(aggDict, ':', '_')

        print(self.toString(aggDict))
        self.pushDict('citations_s1', aggDict)

    def toString(self, aggDict):
        srcp = aggDict['src_paper_title']
        targp = aggDict['targ_paper_title']
        srca = aggDict['src_author_indexed_name']
        targa = aggDict['targ_author_indexed_name']
        return 'Source: ' + str(srca) + ' / ' + str(srcp) + ' ------------- ' + 'Target: ' + str(targa) + ' / ' + str(targp)

    def pushDict(self, table, d):
        conn = pymysql.connect(HOST, USER, PASSWORD, DBNAME)
        cur = conn.cursor()

        keys = d.keys()
        vals = d.values()
        vals = ['"' + v + '"' for v in vals]
        command = "REPLACE INTO %s (%s) VALUES(%s)" % (
            table, ",".join(keys), ",".join(vals))
        cur.execute(command)
        conn.commit()
        cur.close()
        conn.close()

    #OLD CODE DO NOT USE
    #enters a citation record into database
    def pushCitation(self, srceid, targeid, src_ttl, targ_ttl):
        t1 = None
        t2 = None
        if src_ttl:
            t1 = src_ttl[:20]
        if targ_ttl:
            t2 = targ_ttl[:20]
        print('Push citation: ' + str(t1) + "------" + str(t2))
        return

    #enters an author record into database
    def pushAuthor(self, record_dict):
        print('Push Author')
        if 'surname' in record_dict:
            print(record_dict['eid'] + ' ' + record_dict['surname'] + ' ' + record_dict['initials'])
        else:
            print(record_dict)
        return

    # enters a paper record
    def pushPaper(self, record_dict):
        print('Push Paper')
        if 'title' in record_dict:
            print(record_dict['eid'] + ' ' + record_dict['title'])
        else:
            print(record_dict)
        return

    def pushAuthorPaper(self, authid, eid, author_name, paper_name):
        ttl = None
        if paper_name:
            ttl = paper_name[:20]
        print('Push Author-Paper: ' + str(author_name) + "------" + str(ttl))
        return


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
            citedbys = self.sApi.getCitingPapers(eid, num=cite_num)

            # Puts the citing papers of the authors papers, and those respective authors
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
        srcAuthors = self.getAuthorsFromPaper(srcPaperDict)
        targAuthors = self.getAuthorsFromPaper(targPaperDict)

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


    ### OLD CODE NOT USED BELOW
    # this should be the only method that the client interacts with
    def storeAuthorMainOLD(self, auth_id, start_index=0, pap_num=100, cite_num=100, refCount=-1):
        # Puts the main author record
        print('Storing author ' + str(auth_id))
        author = self.storeAuthorOnly(auth_id)
        # Puts the authors papers
        print('Getting author papers')
        papers = self.sApi.getAuthorPapers(auth_id, start=start_index, num=pap_num)
        for eid in papers:
            print('Beginning processing for paper: ' + eid)
            print('Storing into database...')
            main_title = self.storePapersOnly(eid)
            references = self.sApi.getPaperReferences(eid, refCount=refCount)
            getPaperReferences(eid)
            citedbys = self.sApi.getCitingPapers(eid, num=cite_num)

            # Puts the citing papers of the authors papers, and those respective authors
            print('Handling citing papers...')
            for citing in citedbys:
                citing_title = self.storePapersOnly(citing)
                self.storeCitation(citing, eid, citing_title, main_title)
            print('Done citing papers.')

            # Puts the cited papers of the authors papers, and those respective authors
            print('Handling references...')
            for ref in references:
                ref_title = self.storePapersOnly(ref['eid'])
                self.storeCitation(eid, ref['eid'], main_title, ref_title)
            print('Done references')

    # given author id, puts only an author record in db
    def storeAuthorOnly(self, auth, atype='get'):
        author = None
        if atype != 'get':
            author = auth
        else:
            author = self.sApi.getAuthorMetrics(auth)
        self.dbi.pushAuthor(author)

        if 'surname' in author and 'initials' in author:
            return author['initials'] + ' ' + author['surname']
        elif 'surname' in author:
            return author['surname']
        else:
            return None


    # given paper eid, stores the paper in db, as well as author-paper relation
    def storePapersOnly(self, eid):
        paperDict = self.sApi.getPaperInfo(eid)
        self.dbi.pushPaper(paperDict)
        count = 0
        title = None
        if 'title' in paperDict:
            title = paperDict['title']
        if 'authors' in paperDict:
            for authid in paperDict['authors']:
                if isinstance(authid, dict):
                    auth_name = self.storeAuthorOnly(authid, 'local')
                    self.dbi.pushAuthorPaper(authid['eid'], eid, auth_name, title)
                else:
                    auth_name = self.storeAuthorOnly(authid)
                    self.dbi.pushAuthorPaper(authid, eid, auth_name, title)
                count += 1

        if count is 0:
            self.dbi.pushAuthorPaper('NOAUTHOR_' + eid, eid, None, title)
        return title


    # given the src/targ eids, stores the citation relation into db
    def storeCitation(self, src_eid, targ_eid, src_ttl, targ_ttl):
        self.dbi.pushCitation(src_eid, targ_eid, src_ttl, targ_ttl)



#sal = ScopusApiLib()
#k = sal.getAuthorMetrics(22954842600)
#k= sal.getAuthorPapers("AUTHOR_ID:22954842600", 0, 2)
#k = sal.getCitingPapers('2-s2.0-79956094375')
#k = sal.getPaperReferences('2-s2.0-79956094375')
#k = sal.getPaperInfo('2-s2.0-79956094375')
# print(sal.prettifyJson(k))
# k = sal.getPaperInfo('2-s2.0-84992381851')
# print(sal.prettifyJson(k))

# atd = ApiToDB()
# atd.storeAuthorMain(22954842600, 0,1,5)
