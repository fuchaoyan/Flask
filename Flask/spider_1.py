import random
import urllib
import csv
from ip_spider import get_ip_list,get_random_ip
import  requests
import  re
import  os
from pybloom_live import ScalableBloomFilter
import time
from bs4 import BeautifulSoup
from filesimhash import simhash

path='D://search_test3//'
if not os.path.isdir(path):
    os.makedirs(path)


header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Connection': 'close',#访问太多被封
'X-Requested-With': 'XMLHttpRequest',
'Referer': 'http://auto.sina.com.cn/service/r/',

    }

passed=ScalableBloomFilter(initial_capacity=100000,error_rate=0.001,mode=ScalableBloomFilter.LARGE_SET_GROWTH)
URLS = []
hed=[]
Hash=[]
#pro=['36.249.109.42:9999', '112.111.217.206:9999', '60.168.206.32:1133', '175.42.158.55:9999', '220.179.214.166:1133', '1.198.72.90:9999', '27.43.190.73:9999', '123.55.101.155:9999', '123.163.118.90:9999', '123.169.98.105:9999', '220.249.149.128:9999', '175.42.123.205:9999', '171.35.173.171:9999', '171.12.115.163:9999', '27.43.191.167:9999', '175.44.108.133:9999', '27.43.190.18:9999', '123.55.98.21:9999', '58.253.156.50:9999', '123.163.115.228:9999', '123.163.118.254:9999', '175.44.109.209:9999', '115.221.242.115:9999', '222.89.32.180:9999', '123.163.115.208:9999', '36.249.48.13:9999', '220.162.14.164:1080', '180.215.225.12:8888', '175.44.109.146:9999', '175.44.109.39:9999', '175.42.68.183:9999', '36.249.118.52:9999', '220.249.149.54:9999', '171.12.115.54:9999', '110.243.17.93:9999', '47.111.80.105:1080', '175.43.156.38:9999', '175.42.158.170:9999', '163.125.248.202:8118', '175.42.158.203:9999', '123.149.137.98:9999', '58.22.177.31:9999', '175.43.56.23:9999', '175.44.109.33:9999', '60.184.115.118:3000', '175.42.129.164:9999', '115.221.243.218:9999', '163.204.95.136:9999', '171.35.170.156:9999', '27.43.188.84:9999', '60.162.67.75:9000', '27.43.186.188:9999', '123.163.116.136:9999', '103.39.214.69:8118', '36.248.133.109:9999', '27.43.190.137:9999', '118.212.105.81:9999', '175.42.129.215:9999', '123.163.117.189:9999', '123.163.115.106:9999', '123.55.106.119:9999', '175.42.122.84:9999', '115.221.243.63:9999', '58.253.155.148:9999', '123.163.115.70:9999', '112.111.217.35:9999', '36.249.49.52:9999', '1.193.245.202:9999', '223.242.224.141:9999', '220.249.149.152:9999', '123.163.121.163:9999', '183.166.170.2:8888', '113.194.30.128:9999', '123.55.114.221:9999', '123.55.106.6:9999', '123.55.106.60:9999', '220.249.149.216:9999', '220.191.45.136:9000', '171.35.167.53:9999', '175.44.108.53:9999']

def remove_empty_line(content):
    r = re.compile(r'''^\s+$''', re.M | re.S)
    s = r.sub('', content)
    r = re.compile(r'''\n+''', re.M | re.S)
    s = r.sub('\n', s)
    #s = re.sub('\s|\t', '', s)
    #s = re.sub(r"</?(.+?)>|&nbsp;|\t|\r", "", s)
    #s= re.sub('[^\w\u4e00-\u9fff]+', "", s)#要不要保留中文标点？
    #s = re.sub('[a-zA-Z’!"#$%&\'()*+,-.<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", s)


    return s

def remove_js_css(content):
    r = re.compile(r'''<script.*?</script>''', re.I | re.M | re.S)
    s = r.sub('', content)
    r = re.compile(r'''<style.*?</style>''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''<!--.*?-->''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''<meta.*?>''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''<ins.*?</ins>''', re.I | re.M | re.S)
    s = r.sub('', s)
    return s

def remove_any_tag(s):
    s = re.sub(r'''<[^>]+>''', '', s)
    #s = re.sub(r"</?(.+?)>|&nbsp;|\t|\r", "", s)
    return s.strip()

def extract_text(content):
    s = remove_empty_line(remove_js_css(content))
    s = remove_any_tag(s)
    s = remove_empty_line(s)
    return s

def extract_a_label(content):
    soup = BeautifulSoup(content, 'html.parser')
    alink = soup.find_all('a')
    t=soup.find_all('title')
    return alink

def simhashfc(hash_i):
    for i in Hash:
        if hash_i.hamming_distance(i)<=3:
            return False
    return True


#f_content=open('D://search-test//1.txt', 'w',encoding='utf8')
def save_content(text,count,i):
    content=extract_text(text)
    chinese=re.sub('[^\w\u4e00-\u9fff]+', "", content)
    hash_i=simhash(content.split())
    if len(chinese)>100 and simhashfc(hash_i):
        if save_url(text, count) is True:
            Hash.append(hash_i)
            f_html = open(path + 'html//' + str(count) + '.txt', 'w', encoding='utf8')
            f_html.write(text)
            f_content = open(path + 'content//' + str(count) + '.txt', 'w', encoding='utf8')
            f_content.write('url:'+str(i)+'\n')
            f_content.write(content)
            f_content.close()
            passed.add(i)
            csvwriter.writerow([count, i])
            return True
        else:
            return  False

f_a = open(path + 'url.csv', 'w', encoding='utf-8',newline='')
csvwriter=csv.writer(f_a)
def save_url(text,count):
    f_u = open(path + 'url//' + str(count) + '.txt', 'w', encoding='utf8')
    alink = extract_a_label(text)
    f=False
    for link in alink:
        a = link.get('href')
        key = link.string
        if key != None and a != None and a.startswith('http'):
            f=True
            f_u.write(a+'\n')
            if a not in passed:
                URLS.append(a)
    f_u.close()
    return f


response=requests.get('https://www.sina.com.cn/',headers=header,verify=False)
response.encoding='utf-8'
retxt=response.text
count=1
save_content(retxt,count,'https://www.sina.com.cn/')

#urls=addurl(file)
while  URLS is  not None and count<10100:
    try:
        i=URLS.pop(0)
        responsex= requests.get(i, headers=header,verify=False,timeout = 2)
        if responsex.status_code==200:
            responsex.encoding = 'utf-8'
            retxtx = responsex.text
            count += 1
            if save_content(retxtx, count,i) is not True:
                count -=1
    except :
        print('error')
        continue
