import heapq
import  os
import jieba
import jieba.analyse
import  copy
import re
import codecs
import math
import numpy as np
import pandas as pd
from collections import Counter
from bs4 import BeautifulSoup
path='D://search_test3'
if not os.path.isdir(path):
    os.makedirs(path)

#方法1
#词w在文档d中的词频tf (Term Frequency)，即词w在文档d中出现次数count(w, d)和文档d中总词数size(d)的比值
#词w在整个文档集合中的逆向文档频率idf (Inverse Document Frequency)，即文档总数n与词w所出现文件数docs(w, D)比值的对数:
#tf - idf模型根据tf和idf为每一个文档d和由关键词w[1]...w[k]组成的查询串q计算一个权值，用于表示查询串q与文档d的匹配度：

#方法2 直接调用结巴的语料库计算 tf-idf 然后计算检索式和文档的余弦相似度
#权重=余弦相似度*PageRank

def get_bd_msg(searchtext,List,wList,pageList):
    #只读取一次 索引表 索引表存在缓存里
    #**** 提取s搜索内容里的特征词 **********************
    def getKeywords(searchtext):
        swords = []
        wordinfo = []
        IDF = []
        #**** 分词，获取词汇列表 *****
        #split_result = jieba.cut(searchtext)
        split_result= jieba.analyse.extract_tags(searchtext, withWeight=True, allowPOS=())
        for i in split_result:
            swords.append(i[0])
            IDF.append(i[1])
        #**** 统计词频TF *****
        c = Counter(swords) # 词典
        #**** 去除停用词(为了提高效率，该步骤放到统计词频之后)
        delStopwords(c)
        #**** 获取topN  n=5 选前5个作为检索词************
        topN = c.most_common(5)
        words_topN = [i[0] for i in topN ] #在topN中是元组
        #遍历索引单词文档

        for line in wList:
            x=line.split(',')
            if x[1]in words_topN:#读入的单词表有空行的话会报错
                wordinfo.append(x)
        return  [wordinfo,IDF,swords]


    # **** 去除停用词 *******************************
    def delStopwords(dict):
        sw_file = codecs.open('data/哈工大停用词表.txt',encoding='utf8')#注意台式机和笔记本位置不同
        stop_words = []
        for line in sw_file.readlines():
            stop_words.append(line.strip())
        #***** 输入参数为list *************
        # if type(dict) is types.ListType:
        if type(dict) is list:
            words = dict
            for word in words:
                if word in stop_words:
                    words.remove(word)
        #***** 输入参数type为 <class 'collections.Counter'>  *****
        else:
            words = copy.deepcopy(list(dict.keys()))
            for word in words:
                if word in stop_words:
                    del dict[word]
        return words



    def getinfolist( wordinfo):
        infolist=[]
        for i in wordinfo:
            x1 = []
            for line in List:
                y=line.split(',')
                if y[0]==i[0]:
                    x1.append(y[1])
            if x1 is not  None:
                infolist.append(x1)
        #如果有多个的话 需要按长度排序 从短的开始求交集
        infolist=sorted(infolist, key=lambda i: len(i))
        print(infolist)
        file_topN=infolist[0]
        for i in range(1,len(infolist)):
            j=list(set(file_topN) & set(infolist[i]))
            # 包含关键词的文档列表取交集
            if j is not None: #防止出现检索出现空值
                file_topN =j
            else:
                file_topN+=i
        print('文件编号检索成功\n')
        #print (' '.join(file_topN))#7777 256 2388 1106 1459 4696 1480 806 6950 828 9457 122 44 2765 1107 930 7791 2264 2389 1493 580 2618 41 9320 8280 801 6378 593 2486 2619 4109 1529 4692 4108 7756 128 2706 7350 1532 2847 6363 3820 3297 7689 7811 212 3232 9327 1 7763 2509 192 1454 1805 916 8844 5481 1448 419 2831 88 7812 184 2263 6091 7764 1488 3487 1912 1490 9204
        return file_topN #<class 'list'>: ['2618', '419', '1480', '2619', '6091', '3487', '9320', '7689', '9457', '1488', '7777', '6363', '88', '9327', '1', '2831', '4692', '1493', '5481', '4696', '1490', '2706', '3820']


    def getpagerank(file_topN):
        pageranks={}
        pagelist=pageList.split(', \'')#第一个网页的PageRank 值前没有空格 记得处理'  \'1\': 2.2068750529315108e-05' 它划分也是 带着 '
        for i in pagelist:
            num=i.split('\':')
            if num[0] in file_topN:
                    pageranks[num[0]]=float(num[1].lstrip())
        print('pagerank读取成功\n')
        return pageranks


    #需要优化 很慢
    def culmatewight2(file_topN,swords,IDF):
        wights=[]
        for i in file_topN:
            content=open(path + '//content//' + i + '.txt', 'r+', encoding='utf8').read()
            keyWord = jieba.analyse.extract_tags(content, topK=100,withWeight=True, allowPOS=())
            wighti = []
            for j in range(0,len(swords)):
                f=True
                for  weight in keyWord: #('中国', 0.01935936490270184) 元组
                    if(weight[0]==swords[j]):
                        f=False
                        wighti.append(weight[1])
                        break
                if f:
                    wighti.append(-IDF[j])#8280 全[0 0,0] 这个文档里 检索词没有排在前500 是不是不重要？ 不重要的话应该赋值为多少？？ 目的是是
            wights.append(wighti)#<class 'list'>: [[0.0331594140603738, 0], [0.033185920386561145, 0]]
        print('检索词在各文本中的tf_idf向量计算成功\n')
        return  wights


    #余弦计算
    def cosine_similarity2(IDF,w):
        Wfile=[]
        for i in w:
            x = np.array(i)
            y = np.array(IDF)
            num = x.dot(y.T)# Cannot cast array data from dtype('float64') to dtype('<U32') according to the rule 'safe'
            denom = np.linalg.norm(x) * np.linalg.norm(y)
            re=num/denom
            Wfile.append(re)
        print('检索词与文本的余弦相似度计算成功\n')
        return Wfile#<class 'list'>: [0.6788056071524298, 0.635119896156552, 0.6388077600908006, 0.635119896156552, 0.6864887321208623, 0.7420007139639709, 0.6788056071524297, 0.635119896156552, 0.68566091762426, 0.7876932508332247, 0.635119896156552, 0.6843927650433205, 0.6788056071524298, 0.9090202804696257, 0.6113782225638741, 0.635119896156552, 0.6750197550991391, 0.6864887321208623, 0.6628393531020289, 0.6628393531020288, 0.6558211167877374, 0.7014348781329934, 0.6748274159725101, 0.635119896156552, 0.9090202804696257, 0.6788056071524297, 0.635119896156552, 0.6351198961565521, 0.635119896156552, 0.662839353102029, 0.635119896156552, 0.878478271417577, 0.6628393531020289, 0.635119896156552, 0.6351198961565521, 0.662839353102029, 0.6351198961565521, 0.6628393531020289, 0.6788056071524295, 0.6788056071524295, 0.635119896156552, 0.6351198961565521, 0.7051109793857298, 0.6843927650433205, 0.6113782225638741, 0.6627319980247178, 0.6351198961565521, 0.7175217549110002, nan, 0.635119896156552, 0.6788056071524295, 0.6351198961565521, 0.6628393531020289, 0.635119896156552, 0.6351198961565521, 0.6788056071524297, 0.635119896156552, 0.6788056071524295, 0.7420007139639709, 0.6351198961565521, 0.6351198961565521, 0.7420007139639709, 0.6788056071524295, 0.667298583993705, 0.8485222297319049, 0.7420007139639709, 0.662839353102029, 0.6351198961565521, 0.6351198961565521, 0.6788056071524297, 0.6628393531020288]

    wor=getKeywords(searchtext)
    swords=wor[2]
    wordinfo = wor[0]
    IDF = wor[1]  # <class 'list'>: [0.1412776783151541, 0.14392916062336125, 0.14538430752721343] g
    file_topN = getinfolist(wordinfo)
    w = culmatewight2(file_topN, swords,IDF)#<class 'list'>: [[0.0331594140603738, 0], [0.033185920386561145, 0]]
    Wfile=cosine_similarity2(IDF,w)
    page = getpagerank(file_topN)

    #把权值和文档编号建立关系=字典
    dictls = dict(zip(file_topN ,Wfile))
    wightdic={}
    hw=[]
    for j in file_topN:
        x=dictls[j]*page[j]
        wightdic[x]=j
        hw.append(x)
    print(wightdic)
    # 直接排序
    #dict = sorted(dictls.items(), key=lambda x: x[1], reverse=True)
    #堆排序 heapq模块有两个函数：nlargest() 和 nsmallest()
    resultTop=heapq.nlargest(40,hw)
    files=[]#<class 'list'>: ['3232', '6950', '122', '122', '1912', '7812', '8844', '7756', '7350', '184', '930', '44', '4109', '806', '2264', '7764', '5481', '5481', '6363', '7777', '9457', '9457', '4692', '1488', '2706', '2831', '1490', '419', '88', '1', '2619', '828', '41', '1107', '1529', '2389', '2847', '6378', '7791', '4108']
    for l in resultTop:
        files.append(wightdic[l])
    print(files)
    return  [files,swords]

class Summary():
    # 切分句子
    def cutSentence(self,text,keywords):
        sents = []
        text = re.sub(r'\n+','。',text)  # 换行改成句号（标题段无句号的情况）
        text = text.replace('。。','。')  # 删除多余的句号
        text = text.replace('？。','。')  #
        text = text.replace('！。','。')# 删除多余的句号
        text = text.replace('\t+','。')
        sentences = re.split(r'。|！|？|】|；|：',text) # 分句'		董方卓：武磊应该去英国 西班牙人已经不...'
        title=sentences[1]
        sentences = sentences[:-1] # 删除最后一个句号后面的空句
        for sent in sentences:
            sent = re.sub('\s|\t', '', sent)
            sent = re.sub(r"</?(.+?)>|&nbsp;|\t|\r|[|]", "", sent)#先分句后再除去 多余的空格
            #sent = re.sub('\t+', '', sent)

            len_sent = len(sent)
            if len_sent < 4:  # 删除换行符、一个字符等
                continue
            # sent = sent.decode('utf8')
            sent = sent.strip('　 ')
            sent = sent.lstrip('【')
            for a in keywords:
                if sent.count(a):#判断索引词有没有出现在该句子里
                    if len(sent) > 100:
                        x = sent.index(a)
                        if  x<60:
                            sent = sent[x:x+40]
                        elif x>=60:
                            sent=sent[x-40:x]
                    sents.append(sent)
                    break
                else:
                    continue
        if len(sents)<1: #有的网页全是图片，含检索词的句子少于4字 被过滤后为空
            sents.append(title)#绝大数网页 这一行都为标题
        return [sentences[0],sents]

    #**** 提取topN句子 **********************
    def getTopNSentences(self,sents,keywords,n=3):
        sents_score = {}
        len_sentences = len(sents)
        #**** 初始化句子重要性得分，并计算句子平均长度
        len_avg = 0
        len_min = len(sents[0])#IndexError: list index out of range 有的网页全是图片，句子少于4字的 被过滤后为空
        len_max = len(sents[0])
        for sent in sents:
            sents_score[sent] = 0
            l = len(sent)
            len_avg += l
            if len_min > l:
                len_min = l
            if len_max < l:
                len_max = l
        len_avg = len_avg / len_sentences
        # print(len_min,len_avg,len_max)
        #**** 计算句子权重得分 **********
        for sent in sents:
            #**** 不考虑句长在指定范围外的句子 ******
            l = len(sent)
            #if l < (len_min + len_avg) / 2 or l > (3 * len_max - 2 * len_avg) / 2:#不
            if l < (len_min + len_avg) / 2 or l > 50:
                continue
            words = []
            sent_words = jieba.cut(sent)
            for i in sent_words:
                words.append(i)
            keywords_cnt = 0
            len_sent = len(words)
            if len_sent == 0:
                continue
            for word in words:
                if word in keywords:
                    keywords_cnt += 1 #考虑改为加关键词的权值
            score = keywords_cnt * keywords_cnt * 1.0 / len_sent #这句话的
            sents_score[sent] = score
            if sents.index(sent) == 0:# 提高首句权重 关键词首次出现
                sents_score[sent] = 1.2 * score
        #**** 排序 **********************
        dict_list = sorted(sents_score.items(),key=lambda x:x[1],reverse=True)
        # print(dict_list)
        #**** 返回topN ******************
        sents_topN = []
        for i in dict_list[:n]:
            sents_topN.append(i[0])
            # print i[0],i[1]
        sents_topN = list(set(sents_topN))
        #**** 按比例提取 **************************
        if len_sentences <= 5:
            sents_topN = sents_topN[:1]
        elif len_sentences < 9:
            sents_topN = sents_topN[:2]
        return sents_topN
    #**** 恢复topN句子在文中的相对顺序 *********
    def sents_sort(self,sents_topN,sentences):
        keysents = []
        for sent in sentences:
            if sent in sents_topN and sent not in keysents:
                keysents.append(sent)
        keysents = self.post_processing(keysents)
        return keysents
    def post_processing(self,keysents):
        #**** 删除不完整句子中的详细部分 ********************
        detail_tags = ['，一是','：一是','，第一，','：第一，','，首先，','；首先，']
        for i in keysents:
            for tag in detail_tags:
                index = i.find(tag)
                if index != -1:
                    keysents[keysents.index(i)] = i[:index]
        #**** 删除编号 ****************************
        for i in keysents:
            # print(i)
            regex = re.compile(r'^一、|^二、|^三、|^三、|^四、|^五、|^六、|^七、|^八、|^九、|^十、|^\d{1,9}、|^\d{1,2} ')
            result = re.findall(regex,i)
            if result:
                keysents[keysents.index(i)] = re.sub(regex,'',i)
        #**** 删除备注性质的句子 ********************
        for i in keysents:
            regex = re.compile(r'^注\d*：')
            result = re.findall(regex,i)
            if result:
                keysents.remove(i)
        #**** 删除句首括号中的内容 ********************
        for i in keysents:
            regex = re.compile(r'^.∗.∗')
            result = re.findall(regex,i)
            if result:
                keysents[keysents.index(i)] = re.sub(regex,'',i)
        #**** 删除来源(空格前的部分) ********************
        for i in keysents:
            regex = re.compile(r'^.{1,20} ')
            result = re.findall(regex,i)
            if result:
                keysents[keysents.index(i)] = re.sub(regex,'',i)
        #**** 删除引号部分********************
        for i in keysents:
            regex = re.compile(r'，[^，]+：$')
            result = re.findall(regex,i)
            if result:
                keysents[keysents.index(i)] = re.sub(regex,'',i)
        return keysents
    def main(self,text,keywords):
        sentences = self.cutSentence(text,keywords)#对文本进行分句
        url=sentences[0][4:]
        sents_topN = self.getTopNSentences(sentences[1], keywords, n=3)
        #print(sents_topN+'\n')
        keysents = self.sents_sort(sents_topN, sentences[1])
        #print(sents_topN + '\n')
        return [url,keysents]

if __name__=='__main__':
    f = open(path + '//nsinfo.csv', 'r', encoding='UTF-8').read()  # 别把读文件放到循环里 慢
    List = f.split('\n')
    fw = open(path + '//nswords.csv', 'r', encoding='UTF-8').read()
    wList = fw.split('\n')
    pageList = open(path + '//summary.txt', 'r', encoding='UTF-8').read()
    summary=Summary()
    #res=get_bd_msg('奔驰与法拉利')
    #keywords=res[1]
    #for i in res[0]:
    keywords=['王牌','西班牙']
    content = open(path + '//content//'+'10057.txt', 'r+', encoding='utf8').read()
    print(summary.main(content,keywords))

