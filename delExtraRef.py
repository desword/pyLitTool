'''
remove the extra elements of the reference in bibtex.
@keywords: is the elements that ready to be removed.

'''

import re
path = r'D:\GitProject\path-profile\Paper_tex\approach.bib'
f = open(path)
line = f.readline()

newFile = []
keywords = ['Address', 'Publisher', 'Url']
while line:
	isFind = False
	for eachKey in keywords:
		if re.findall(eachKey, line):
			isFind = True
			break;
	if isFind == False: # if not find the key, then add current line
		newFile.append(line)
	line = f.readline()

fo = open(r'D:\test.bib' ,'w')
fo.writelines(newFile)