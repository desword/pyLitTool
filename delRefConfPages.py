'''
remove the extra elements of the reference in bibtex.
@keywords: is the elements that ready to be removed.

'''

import re
path = r'E:\github\softhint_2\softhint\paper\softhint.bib'
f = open(path)
line = f.readline()

newFile = []
keywords = ['Pages']
condiWords = ['Journal']
while line:
	isFind = False
	for eachKey in keywords:
		if re.findall(eachKey, line):
			isFind = True
			break;	
	if isFind == False: # if not find pages, then append this line
		newFile.append(line)
	line = f.readline()

fo = open(r'test.bib' ,'w')
fo.writelines(newFile)