#coding:utf-8
import urllib2
import re
'''
sample :
[期刊]
余涛、俞立中、王铮：移动计算环境下GIS技术的发展及应用，载于《测绘通报》，2002年第x期，第x页。
[学位论文]
朱凯：一种基于相似路径集生成的程序故障定位方法，华中科技大学
[专著]

----- using
http://book.douban.com/subject_search?search_text=Android+%E8%BD%AF%E4%BB%B6%E5%AE%89%E5%85%A8&cat=1001
[论文集]

'''
 
def getPublicationVol(html, beg):
    end = len(html)
    edLink =  html.find('</a>',beg, end)
    LinkMat = re.match('', html[beg:edLink])
    pass

def getPaperTitle(html, beg):
    end = len(html)
    aIndex = html.find('<a ',beg , end)
    reaIndex = html.find('</a>',beg, end)
    p = re.compile('<[^>]+>')
    #print p.sub("", html[aIndex:reaIndex])
    return p.sub("", html[aIndex:reaIndex])

def getPaperAuthor(html, beg):
    end = len(html)
    #get author list during <span> label
    spanIndex = html.find('<span>',beg, end)
    respanIndex = html.find('</span>',beg, end)
    p = re.compile('<[^>]+>')
    authorList = []
    #issue1 在找完第一轮作者之后，无法找后面的作者
    while 1:
        aIndex = html.find('<a',spanIndex, respanIndex)
        if aIndex == -1:
            isetc = html.find('...',reaIndex, reaIndex +16)
            #print html[reaIndex: reaIndex + 16]
            if isetc != -1:
                authorList.append('...')                
            break;
        reaIndex = html.find('</a>',spanIndex, respanIndex)
        #print html[aIndex:reaIndex]
        author = p.sub("", html[aIndex:reaIndex])
        authorList.append(author)
        #print author
        #fixed 1, replace aIndex to reaIndex
        spanIndex = reaIndex+3
    return authorList

def getPublicationName(html, beg):
    end = len(html)
    startPubIndex = html.find('</span>',beg, end)
    endPubIndex = html.find('</a>',startPubIndex, end)
    #print html[startPubIndex:end]
    #print html[startPubIndex:end]
    tempList = html[startPubIndex: endPubIndex].split()
    #print tempList
    pubNameMat = re.match('title=\"(.{1,})\"', tempList[-1])
    if pubNameMat:
        pubName = pubNameMat.group(1)
    else:
        pubName = '-*-getPubName Error-*-'
    #print pubName
    return pubName

def getPublicationYear(html,beg):
    end = len(html)
    stIndex = html.find('<span class=\"sc_time\"',beg , end)
    edIndex = html.find('</span>',stIndex, end)
    pbyearMat = re.compile('<[^>]+>')
    #print pbyearMat.sub("", html[stIndex:edIndex])
    return pbyearMat.sub("", html[stIndex:edIndex])

#--issue2 etc do not deal well
#++fixed issue2
def RefenceRegulate(title , authorList, pubName, pubYear):
    ref = ''; etc = ''
    if len(authorList) > 3:
        etc = '等'
        authorList.pop()
    for author in authorList:
        ref += (author + '、')
    ref = ref[:len(ref)-3] + etc + '：'    
    ref += (title + '，'+ '载于' + pubName + '，' + pubYear + '年。')
    print ref
    return ref
    pass
    
if __name__ == '__main__':
    keyword = '民法学研究'
    baidu = 'http://xueshu.baidu.com/s?wd='+ keyword + '&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=0'
    html = urllib2.urlopen(baidu).read()
    beg = 0; count = 0;# count to record 
    end = len(html)
    while 1:
        startString = 'h3 class=\"t c_font\"'
        beg = html.find(startString,beg, end)
        if count == 3:
            break;
        #try to get volume
        vol = getPublicationVol(html, beg)
        #try to get title
        title = getPaperTitle(html, beg)
        #try to get author
        authorList = getPaperAuthor(html, beg)
        #try to get publication name
        pubName = getPublicationName(html, beg)
        #try to get years
        pubYear = getPublicationYear(html,beg)
        
        RefenceRegulate(title , authorList, pubName, pubYear)
        beg += len(startString)
        count += 1
