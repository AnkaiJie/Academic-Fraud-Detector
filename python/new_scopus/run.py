from apilib import *

# sal = ScopusApiLib()
# k = sal.getPaperInfo('2-s2.0-79956060771')
#k = sal.getAuthorMetrics(22954842600)
# print(sal.prettifyJson(k))

atd = ApiToDB()
atd.storeAuthorMain(22954842600, start_index=0, pap_num=1, cite_num=5)
