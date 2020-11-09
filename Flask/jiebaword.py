import jieba
from pybloom_live import ScalableBloomFilter

path='D://search_test3//'
#break_words=[]
break_words=ScalableBloomFilter(initial_capacity=100000,error_rate=0.001,mode=ScalableBloomFilter.LARGE_SET_GROWTH)

#判断是否为中文
def is_chinese(words):
    for word in words:
        if not (u'\u4e00' <= word <= u'\u9fa5'):
            return False
    return True
#删除停用词
def get_break_stopWords():
    with open('data/哈工大停用词表.txt', 'r', encoding='UTF-8-sig') as f:
        for line in f:
            break_words.add(line.replace('\n', ''))
    f.close()
 # 删除停用词以及非中文
def delete_break_words( word):
    if word not in break_words:
        if is_chinese(word):
            return word

def jie_ba(test):
    #结巴分词
    seg_list = []  # 默认是精确模式
    for i in jieba.cut(test,cut_all=True):
        word2 = delete_break_words(i)
        if word2:
            seg_list.append(word2)
    return seg_list

if __name__=="__main__":
    count=1
    get_break_stopWords()
    while count<20001:
        file_text = open(path + 'jiebaword//' + str(count)+'.txt', 'w', encoding='utf8')
        f_content = open(path + 'content//' + str(count) + '.txt', 'r+', encoding='utf8')
        while True:
            text=f_content.readline()
            if text:
                words2 = jie_ba(text)
                file_text.write("/ ".join(words2))
            else:
                break
        file_text.close()
        f_content.close()
        count+=1
