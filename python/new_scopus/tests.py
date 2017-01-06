def changeValue(d):
	for key, val in d.items():
		if '"' in val:
			print('un here')

			d[key] = val.replace('"', '\\' + '"')


k={'lmao': 'dsfjslkad "game" d fskj'}

changeValue(k)
print(k)