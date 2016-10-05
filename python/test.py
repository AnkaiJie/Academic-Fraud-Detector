import re
k = '[sdsdsd][sd]title here'
print(re.sub('(\[.*\])', '', k))
print(k)

