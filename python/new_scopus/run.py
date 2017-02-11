from apilib import *

# sal = ScopusApiLib()
# k = sal.getPaperReferences('2-s2.0-84949209479')
# print(len(k))
# print(sal.prettifyJson(k))



atd = ApiToDB()
atd.storeAuthorMain(7006619672, start_index=23, pap_num=33, cite_num=100)
