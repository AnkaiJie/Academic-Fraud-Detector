'''
Created on Jan 28, 2016

@author: Ankai
'''

import re


pattern = "asd: s"
print(pattern)
pattern = re.sub(r'\W+', ' ', pattern)
pattern = "+".join(pattern.split())
print(pattern.find('sd'))


print("min chen".split(","))