from apilib import *

# sal = ScopusApiLib()
# k = sal.getPaperReferences('2-s2.0-79956094375')
# print(len(k))
# print(sal.prettifyJson(k))



atd = ApiToDB()
atd.storeAuthorMain(22954842600, start_index=0, pap_num=50, cite_num=100)
