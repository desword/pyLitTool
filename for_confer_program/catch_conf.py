import urllib2
import re
import time
from lxml import etree
import msvcrt

def checkprogram(confSite, startStr, badContent):
    # confSite = "http://sensys.acm.org/2018/program/"

    html = urllib2.urlopen(confSite).read()
    # startStr = "/html/body/div/div/div/article"
    # badContent = "TBA"


    selector = etree.HTML(html)
    result =  selector.xpath(startStr + "/text()")
    noTBA = True
    for eachLine in result:
        try:
            eachLine.index(badContent)
            noTBA = False
            print "[-]", confSite,", -- no program yet"
            return;
        except:
            pass;

    print "[*]", confSite, ", ++update!"




confListFile = "confList.txt"
f = open(confListFile)
lines = f.readlines()
for line in lines:
    sptmp = line.split(",")
    confSite =  sptmp[0]
    startStr = sptmp[1]
    badContent = sptmp[2]
    checkprogram(confSite, startStr, badContent)

# print html


msvcrt.getch()