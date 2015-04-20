# -*- coding: utf-8 -*-
import urllib2
import re
import time
'''
sample :
[期刊]
余涛、俞立中、王铮：移动计算环境下GIS技术的发展及应用，载于《测绘通报》，2002年第x期，第x页。
[学位论文]
朱凯：一种基于相似路径集生成的程序故障定位方法，华中科技大学，XX省：2008年，第x页。
[专著]

----- using
http://book.douban.com/subject_search?search_text=Android+%E8%BD%AF%E4%BB%B6%E5%AE%89%E5%85%A8&cat=1001
[论文集]

'''
 
def getPublicationVol(html, beg):
    end = len(html)
    edLink =  html.find('</a>',beg, end)
    LinkList = html[beg:edLink].split()
    st = LinkList[3]
    #print st[6:len(st)-1]
    Volhtml = urllib2.urlopen(st[6:len(st)-1]).read()
    #print Volhtml
    LinkMat = re.match(' herf=\"(.{1,})\" ', html[beg:edLink])
    if LinkMat:
        print LinkMat.group(1)
    else:
        print '[-]get vol link error'
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
        spanIndex = reaIndex+3
    return authorList

def getPublicationName(html, beg, cate):
    end = len(html)
    startPubIndex = html.find('</span>',beg, end)
    endPubIndex = html.find('</a>',startPubIndex, end)
    tempList = html[startPubIndex: endPubIndex].split()
    if cate == 0:
        pubNameMat = re.match('title=\"(.{1,})\"', tempList[-1])
        if pubNameMat:
            pubName = pubNameMat.group(1)
        else:
            pubName = '[-]getPubName Error'
    else:
        pubNameMat = re.match('</span>&nbsp;-&nbsp;(.{1,})&nbsp;-&nbsp;<span',tempList[0])
        if pubNameMat:
            pubName = pubNameMat.group(1)
        else:
            pubName = '[-]get thesis error'
    return pubName

def getPublicationYear(html,beg):
    end = len(html)
    stIndex = html.find('<span class=\"sc_time\"',beg , end)
    edIndex = html.find('</span>',stIndex, end)
    pbyearMat = re.compile('<[^>]+>')
    #print pbyearMat.sub("", html[stIndex:edIndex])
    return pbyearMat.sub("", html[stIndex:edIndex])

#check the paper refer is from thesis or magzine
#0-> magzine, 1 -> thesis
def checkRefCate(html, beg):
    end = len(html)
    startPubIndex = html.find('</span>',beg, end)
    endPubIndex = html.find('</a>',startPubIndex, end)
    tempList = html[startPubIndex: endPubIndex].split()
    pubNameMat = re.match('</span>&nbsp;-&nbsp;(.{1,})&nbsp;-&nbsp;<span',tempList[0])
    if pubNameMat:
        return 1
    else:
        return 0

def RefenceRegulate(title , authorList, pubName, pubYear, cate):
    if cate == 0:
        ref = ''; etc = ''
        if len(authorList) > 3:
            etc = '等'
            authorList.pop()
        for author in authorList:
            ref += (author + '、')
        ref = ref[:len(ref)-3] + etc + '：'    
        ref += (title + '，'+ '载于' + pubName + '，' + pubYear + '年第x期，第x页。')        
    else:
        pubName = pubName.strip()
        pubName = pubName.lstrip('《')        
        pubName = pubName.rstrip('》')
        ref = authorList[0] + '：' + title + '，' + pubName + '，xx省：' + pubYear + '年，第x页。'         
    #print ref    
    return ref

def url_user_agent(url):
    proxy_handler = urllib2.ProxyHandler({"http" : "127.0.0.1:8087"})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    #i_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    response = urllib2.urlopen(req)
    #print response.read()
    return response.read()

def getRefer(keyword ):
    #keyword = '一种基于相似路径'
    #print keyword
    
    #keyword = '用益物权'
    #baidu = 'http://xueshu.baidu.com/s?wd='+ keyword + '&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=0'
    baidu = 'http://xueshu.baidu.com/s?wd='+ keyword + '&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D'
    #html = url_user_agent(baidu)
    html = urllib2.urlopen(baidu).read()
    #print 'html:' + html
    beg = 0; count = 0;# count to record 
    end = len(html); cate = 0
    referList = []
    while 1:
        startString = 'h3 class=\"t c_font\"'
        beg = html.find(startString,beg, end)
        if count == 3 or beg < 0:
            print count, beg
            break;
        #try to get volume
        #[-]volume some error
        #vol = getPublicationVol(html, beg)
        cate = checkRefCate(html, beg)
        #try to get title
        title = getPaperTitle(html, beg)
        #try to get author
        authorList = getPaperAuthor(html, beg)
        #try to get publication name
        pubName = getPublicationName(html, beg, cate)
        #try to get years
        pubYear = getPublicationYear(html,beg)        
        referList.append(RefenceRegulate(title , authorList, pubName, pubYear, cate))
        beg += len(startString)
        count += 1
    return referList

def savePapers(useList):
    fileName = time.strftime('%Y-%m-%d_%H-%M',time.localtime(time.time())) + '.txt'
    f = open(fileName,'w')
    for tl in list:
        f.write(tl + '\n')
    f.close() 
    print ('检索的文献已经存储在当前文件夹的%s里面啦！' % (fileName)).decode('utf-8').encode('mbcs') 

if __name__ == '__main__':
    '''
    keyword = raw_input()
    tempList = getRefer(keyword.decode('mbcs').encode('utf-8'))
    index = 0
    for tl in tempList:
        st = '[%d]%s' % (index,tl)
        
        print st.decode('utf-8').encode('mbcs')
        index += 1
    '''
    list = []; tempList = []
    choice = 0
    print '~欢迎使用参考文献自动生成系统 V1.0 哟~'.decode('utf-8').encode('mbcs')    
    print '~请保证联网状态哈O(∩_∩)O哈！'.decode('utf-8').encode('mbcs')
    print '~目前仅支持检索期刊和学位论文哈~ 专著，会议的论文，等我后续搞定！'.decode('utf-8').encode('mbcs') 
    while 1:
        print '请选择指令：'.decode('utf-8').encode('mbcs') 
        print '             1. 检索文献'.decode('utf-8').encode('mbcs') 
        print '             2. 已经检索的文献'.decode('utf-8').encode('mbcs')
        print '             3. 保存检索好的文献'.decode('utf-8').encode('mbcs')
        print '             4. byebye啦！'.decode('utf-8').encode('mbcs') 
        choice = raw_input()
        if choice == '1':
            while 1:
                print '请输入文献名称：'.decode('utf-8').encode('mbcs') 
                keyword = raw_input()
                #print 'in:' + keyword
                #print '杨代雄'
                tempList = getRefer(keyword.decode('mbcs').encode('utf-8'))
                #print tempList
                index = 0
                for tl in tempList:
                    print ('[%d]%s' % (index,tl)).decode('utf-8').encode('mbcs') 
                    index += 1
                if index == 0:
                    print '没有搜索到文献呀，换个试下？(y/n)'.decode('utf-8').encode('mbcs') 
                    trya= raw_input()
                    if trya == 'n' or trya == 'N':
                        break;
                    continue
                print '请选择正确的文献：'.decode('utf-8').encode('mbcs') 
                index = raw_input()
                list.append(tempList[int(index)])
                print ('选择了：' + ('[%s]%s' % (index,tl))).decode('utf-8').encode('mbcs') 
                print '继续检索吗？（y/n）'.decode('utf-8').encode('mbcs') 
                yorn = raw_input()
                if yorn == 'n' or yorn == 'N':
                    break;
        elif choice == '2':
            print '现在存储的文献有：'.decode('utf-8').encode('mbcs') 
            index = 0
            for tl in list:
                print ('[%d]%s' % (index,tl)).decode('utf-8').encode('mbcs') 
                index += 1
        elif choice == '3':
            savePapers(list)
        elif choice == '4':
            print '确保所有文献都存好了哟！~存好了(y),没存好(n)'.decode('utf-8').encode('mbcs')
            input = raw_input()
            if input == 'y' or input == 'Y':
                break;
            savePapers(list)            
        else:
            print '没有这个指令，又卖萌啦~?(^?^*)'.decode('utf-8').encode('mbcs') 
            
            





    
    

