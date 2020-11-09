import csv
# 根据正排索引形成倒排索引
def get_word_index(index_lst):
    length = len(index_lst)
    # 遍历每一个文档
    for i in range(length):
        index_item = index_lst[i]
        # 遍历每一个文档里面的每一个单词
        for j in index_item[1]:
            flag = -1
            # 将文档中的单词和已存的单词列表的单词进行比较
            # 没有存在则添加
            word_len = len(word_lst)
            for t in range(word_len):
                if j[0] == word_lst[t][1]:
                    flag = t
                    break
            if flag == -1:
                word_item = []
                word_item.append(word_len)
                word_item.append(j[0])
                word_item.append(1)
                word_item.append(1)
                word_lst.append(word_item)
                invert_index_item = []
                invert_index_item.append(word_len)#单词
                invert_index_item.append(index_item[0])#文档编号
                invert_index_item.append(j[1])#频率
                invert_index_item.append(j[2])#位置
                invert_index.append(invert_index_item)
            else:
                word_item = word_lst[flag]
                word_item[2] += 1
                invert_index_item = []
                invert_index_item.append(flag)
                invert_index_item.append(index_item[0])
                invert_index_item.append(j[1])
                invert_index_item.append(j[2])
                invert_index.append(invert_index_item)
    #排序，将invert_index 设置为根据单词id排序
    invert_index.sort(key=lambda x:x[0])
    # 设置每个单词后的偏移量
    offset = 0
    word_lst[0][3] = offset
    offset += 1
    ids=invert_index[offset][0]
    for i in range(1,len(word_lst)):
        # 当前一个和当前不相等的时候记录偏移量
        #while invert_index[offset - 1][0] == invert_index[offset][0]:
            #offset += 1
        #word_lst[i][3] = offset

        # 单词i 的偏移量 = 单词 i-1 的 词频+ 单词 i-1 的偏移量
        word_lst[i][3] = word_lst[i-1][2]+word_lst[i-1][3]



# 根据一篇文档形成正排索引
def get_doc_index(text_str):
    text_lst = text_str.split('/')
    # text_str = text_str.replace('/','')
    index = 1
    length = len(text_lst)
    doc_lst = []
    # 遍历文档的所有词
    for i in range(length):
        flag = -1
        # 比较文档里面的这个词是否是已经记录的，是则返回下标
        for j in range(len(doc_lst)):
            if text_lst[i] == doc_lst[j][0]:
                flag = j
                break
        # 若第一次出现，则生成新的词的信息
        if flag == -1:
            word_info = []
            word_info.append(text_lst[i])
            word_info.append(1)
            hitlist = []
            hitlist.append(index)
            word_info.append(hitlist)
            doc_lst.append(word_info)
        # 不是则数量加一，并增加下个词的位置
        else:
            word_info = doc_lst[flag]
            word_info[1] += 1
            word_info[2].append(index)
        index += len(text_lst[i])
    # 遍历所有词，让每个词中，记录的位置都是与上个词的差值
    for i in doc_lst:
        if i[1] == 1:
            continue
        if i[1] == 2:
            i[2][1] = i[2][1] - i[2][0]
            continue
        for j in range(i[1]-1,1,-1):
            i[2][j] = i[2][j] - i[2][j-1]
    return doc_lst
path='D://search_test3//'
fwords = open(path +'nswords.csv', 'w+', encoding='utf8',newline='')#open('xxx.csv', 'w', newline='') # 可行避免出现空行
fsinfo = open(path + 'nsinfo.csv', 'w+', encoding='utf8',newline='')
wordwriter=csv.writer(fwords)
infowriter=csv.writer(fsinfo)
wordwriter.writerow(['单词ID','单词','单词频率','偏移量（文档频率）'])
infowriter.writerow(['单词ID','文档编号','词出现的频率','词在文档中出现的位置'])
if __name__ == '__main__':
    count = 1
    word_lst = []
    invert_index = []
    index_list=[]
    while count<=10000:
        doc_list=[]
        f_content = open(path + 'jiebaword//' + str(count) + '.txt', 'r', encoding='utf-8').read()
        word_lstitem=get_doc_index(f_content)
        doc_list.append(count)
        doc_list.append(word_lstitem)
        index_list.append(doc_list)
        count += 1
    get_word_index(index_list)
    for i in word_lst:
        wordwriter.writerow(i)
    for i in invert_index:
        infowriter.writerow(i)
    fsinfo.close()
    fwords.close()


