 # -*- coding: utf-8 -*-
import os
import time
import random

'''
filePath = ''
st = os.stat(fileName)
modifyName = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(st.st_mtime))
'''

#param path: files location
#param exp: extend type of files
#path = r'C:\Users\Administrator\Documents\Tencent Files\1428719317\FileRecv\MobileFile'
#path = 'D:\\DCIM'
path= r'C:\Users\Administrator\Pictures\graduate'
exp = '.jpg'
for root, dirs, files in os.walk(path):
    for fn in files:
        st = os.stat(root + '\\' + fn)
        modifyName = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(st.st_mtime))
        #print root + '\\' + fn,root + os.sep + modifyName + exp
        try:
            os.rename(root + '\\' + fn,root + os.sep + modifyName + exp)
        except:
            r = '%d' %random.randint(1,1000)
            print r
            os.rename(root + '\\' + fn,root + os.sep + modifyName + r + exp)
        print root, fn, modifyName
