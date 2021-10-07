# -*- coding: utf-8 -*-   


import os.path, time, os
import random
 
class TypeError (Exception):
    pass


def samefiledeal(files_input):

    tm22 = files_input

    while True:
        if os.path.exists(tm22):
            tm22 = tm22 +"_"+ str(random.randint(0, 100))
        else:
            break;
    return tm22
    

folder = "./"


for root, dirs, files in os.walk(folder):  
    print(root) #当前目录路径  
    print(dirs) #当前路径下所有子目录  
    print(files) #当前路径下所有非目录子文件

    for eachf in files:

        extend_str = ""

        print(eachf)
        if ".py" in eachf:
            continue;
        if ".MP4" in eachf:
            extend_str = ".MP4"
        if ".JPG" in eachf:
            extend_str = ".JPG"
            
        filemt= time.localtime(os.stat(eachf).st_mtime)
        tm1 = time.strftime("%Y%m%d-%H%M%S",filemt)
        
        tm1 =samefiledeal(tm1)

        tm2 = tm1+extend_str

        os.rename(eachf , tm2)






