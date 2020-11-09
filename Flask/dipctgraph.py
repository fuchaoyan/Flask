from pygraph.classes.digraph import digraph
import jieba
from pybloom_live import ScalableBloomFilter
from pygraph.classes.digraph import digraph

from copy import deepcopy
path='D://search_test3//'
lin = open(path  + 'lins.txt', 'w+', encoding='utf8')
dicf = open(path  + 'dics.txt', 'w+', encoding='utf8')
dics=ScalableBloomFilter(initial_capacity=100000,error_rate=0.001,mode=ScalableBloomFilter.LARGE_SET_GROWTH)
dic1=[]
dic2=[]
#构图有要求 第1行空 第3行空 节点最后不能重复和有空格
lin.write('\n')
for i in range(1,10001):#就先跑10000试试 没有出链的
    dic1.append(str(i))
    if i < 10000:
        lin.write(str(i) + ' ')
    else:
        lin.write(str(i))
lin.write('\n'+'\n')
def buliddic():
    with open(r'D:/search_test3/url.txt', 'r',
              encoding='utf-8') as f:
        txt = f.read()  # 读取所有数据
    lines = txt.split('\n')  # 拆分
    for i in lines:
        ID = i.split(',')  # 得到节点列表
        if ID[-1] is not None:
            dic2.append((ID[-1]))
            dics.add(ID[-1])
    dictls = dict(zip(dic2 ,dic1))
    print(len(dictls))
    print(dictls,file=dicf)
    return  dictls

def bulidgraph():
    count=1
    Dicts = buliddic()
    lines=[]
    while count<=10000:
        file_text = open(path + 'url//' + str(count) + '.txt', 'r+', encoding='utf8')
        txt = file_text.read()  # 读取所有数据
        s = []
        if txt is not None:
            for i in  txt.split('\n'):
                if i in Dicts and i is not  None:
                    x=[str(count),Dicts[i]]
                    if x not in s:
                        s.append(x)
                        print(str(count),Dicts[i],file=lin)
                else:
                    continue
            lines=lines+s
        count+=1
    print(len(lines))
    return lines
if __name__ == '__main__':
    s=bulidgraph()
    print(s)