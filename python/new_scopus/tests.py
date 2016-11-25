
def addPrefixToKeys(dOrig, prefix):
    d = dict(dOrig)
    keys = list(d.keys())
    for key in keys:
        print(key)
        d[prefix+key] = d.pop(key)
    return d

k = {'coverDate': '2017-11-01', 'title': 'Certificateless authentication protocol for wireless body area network', 'eid': '2-s2.0-84992381851', 'publicationName': 'Advances in Intelligent Systems and Computing'}
d = addPrefixToKeys(k, 'test_')
print(d)
