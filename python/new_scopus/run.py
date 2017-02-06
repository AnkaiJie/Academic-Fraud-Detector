from apilib import *

# sal = ScopusApiLib()
# k = sal.getPaperReferences('2-s2.0-84947445471')
# k = sal.getCitingPapers('2-s2.0-79956094375')
# i = 1
# while (i < 80):
# 	print(i)
# 	k = sal.getCitingPapers('2-s2.0-79956094375', num=1)
# 	i += 1
# print(sal.prettifyJson(k))



atd = ApiToDB()
atd.storeAuthorMain(22954842600, start_index=0, pap_num=50, cite_num=100)
