from flask import Flask, request
from  search0 import  get_bd_msg,Summary
from  flask import  render_template
path='D://search_test3'
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('web.html')
@app.route('/s')
def search():
    path = 'D://search_test3'
    word = request.args.get('wd')
    print(word)
    res=get_bd_msg(word,List,wList,pageList )
    summary = Summary()
    keywords = res[1]
    txts=[]
    for i in res[0]:
        content = open(path + '//content//' + str(i) + '.txt', 'r+', encoding='utf8').read()
        txt=summary.main(content, keywords)
        txts.append(txt)
        print(txt)
    tr='查询结果\n'
    return render_template('web.html', str=tr, li=txts)



if __name__=='__main__':
    f = open(path + '//nsinfo.csv', 'r', encoding='UTF-8').read()  # 别把读文件放到循环里 慢
    List = f.split('\n')
    fw=open(path + '//nswords.csv', 'r', encoding='UTF-8').read()
    wList = fw.split('\n')
    pageList = open(path + '//summary.txt', 'r', encoding='UTF-8').read()
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)