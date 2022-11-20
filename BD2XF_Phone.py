# -*- coding: utf-8 -*-
"""
@Time ： 2022/2/21 18:52
@Auth ： jxwang17
@File ：downBD_audio.py
@IDE ：PyCharm
@Motto：UTF-8

"""
import getpass
import requests
import re
import os
import time
import sys
import random                                                 #随机
from selenium import webdriver                                #selenium控制浏览器
from selenium.webdriver.chrome.options import Options         #设置浏览器参数
from selenium.webdriver.support.wait import WebDriverWait



def save_file(filename, content):
   """保存音乐"""
   with open(file=filename, mode="wb") as f:
       f.write(content)

def down(sorce_phonetic):

    # url = "https://www.oxfordlearnersdictionaries.com/definition/english/" + sorce_phonetic.strip()
    url = "https://fanyi.baidu.com/?aldtype=85#en/zh/" + sorce_phonetic.strip()
    wbdata = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}).text
    phon_cont = re.findall('data-src-mp3="(.*?)" data-src-ogg=',wbdata)
    print((wbdata))
    # phon_cont = ['https://www.oxfordlearnersdictionaries.com/media/english/uk_pron/c/cpr/cpr__/cpr__gb_1.mp3', 'https://www.oxfordlearnersdictionaries.com/media/english/us_pron/c/cpr/cpr__/cpr__us_1.mp3']

    #下载音频
    for i in phon_cont:
        file_name = ''
        if 'uk_pron' in i:
            file_name = 'audio\\'+sorce_phonetic+'_ENG.mp3'
        if 'us_pron' in i:
            file_name = 'audio\\' + sorce_phonetic + '_USA.mp3'

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        response = requests.get(i,headers=headers)
        content = response.content
        save_file(file_name, content)

def getmap(indicpath):
    rfile = open(indicpath,'r',encoding='utf-8').readlines()[1:]
    IPAdic,DJdic,KKdic,IPAtmpdic,DJtmpdic,KKtmpdic = {},{},{},{},{},{}
    for line in rfile:
        IPAtmpdic[line.split('\t')[0].strip()] = line.split('\t')[1].strip()
        DJtmpdic[line.split('\t')[3].strip()] = line.split('\t')[2].strip()
        KKtmpdic[line.split('\t')[5].strip()] = line.split('\t')[4].strip()

    for i in sorted(IPAtmpdic,key=lambda x:len(x),reverse=True):IPAdic[i] = IPAtmpdic[i]
    for i in sorted(DJtmpdic,key=lambda x:len(x),reverse=True):DJdic[i] = DJtmpdic[i]
    for i in sorted(KKtmpdic,key=lambda x:len(x),reverse=True):KKdic[i] = KKtmpdic[i]
    return IPAdic,DJdic,KKdic


def down_v1():
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[4]').click()  #翻译
    phonecont,translation = '',''
    driver.implicitly_wait(5)
    text1 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div[4]/div[1]/div[3]/div/div[2]/div/div[1]/div[1]/div[1]/div/span[1]/b')
    text2 = driver.find_elements_by_class_name('phonetic-transcription')
    for i in text2:
        print(i.text)
    print(text1.text)
    # text3 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div[4]/div[1]/div[3]/div/div[2]/div/div[1]/div[1]/div[1]/div/span[1]/b')
    # translation =text3.text
    # # phonecont = re.sub('\[\]ˌˈ',' ','%s\t&\t%s'%(text1.text,text2.text)).replace('ː',':')
    # phonecont = re.sub('\[\]ˌˈ',' ','%s\t'%(text1.text)).replace('ː',':')
    # except:
    #     print('%s：单词文本无对应音标，请检查~'%(sorce_phonetic))
    # print(phonecont,translation)
    # return phonecont,translation.strip('\n')

def loopfild(phonecont,IPAdic):
    if phonecont != '':
        engph = re.sub('[\[\]ˌˈ]',' ',phonecont.split('\r\n')[0].split(' ')[1]).lstrip().rstrip().replace('ː',':')        # ə kaʊntə bɪləti
        # usaph = re.sub('[\[\]ˌˈ]',' ',phonecont.split('\r\n')[1].split(' ')[1]).lstrip().rstrip().replace('ː',':')        # ə kaʊntə bɪləti
        switlst = []
        for n, i in enumerate(engph):
            if n <= len(engph) - 2:
                str = i + engph[n + 1]
                if str in IPAdic:
                    # print('Y',n,str,n+len(str)-1)
                    switlst.append('%s\t%s&%s'%(str,n,n+len(str)-1))
                else:
                    # print('N',n,i)
                    switlst.append('%s\t%s'%(i,n))
            else:
                # print('A',n,i)
                switlst.append('%s\t%s'%(i,n))

        newlst,dic = [],{}
        for onestr in switlst:
            value = onestr.split('\t')[0]
            key = onestr.split('\t')[1]
            if '&' in onestr:
                dic[key.split('&')[0]] = value
                dic[key.split('&')[1]] = ' '
            else:
                if key not in dic:
                    dic[key] = value
        resstr = ''
        for k,v in dic.items():
            if v != ' ':
                resstr += IPAdic[v]+' '
        return resstr

if __name__ == '__main__':
    indicpath = r'.\PhoneMap.txt'
    IPAdic,DJdic,KKdic = getmap(indicpath)

    wordlst = sys.argv[1]

    rlst = open(wordlst,'r',encoding='utf-8').readlines()
    wres = open('00_音标结果.lst','w+',encoding='utf-8')
    oneinfo = {}
    for line in rlst:
        if line not in ['\r\n','\n',''] and '#' not in line:
            if '\t' in line:
                if line.split('\t') != 1:oneinfo[line.split('\t')[0].lower()] = line.split('\t')[1].strip()
            else:oneinfo[line.strip()] = ''

    print(oneinfo)
    ''''''
    for oneword,engph in oneinfo.items():
        chrome_options = Options()  # Options类实例化
        # # 设置浏览器参数
        chrome_options.add_argument('--headless')    # --headless是不显示浏览器启动及执行过程
        chrome_options.add_argument('lang=zh_CN.utf-8')  # # 启动时设置默认语言为中文 UTF-8
        UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'  # # user-agent用来模拟移动设备,设置lang和User-Agent信息，防止反爬虫检测
        chrome_options.add_argument('User-Agent=' + UserAgent)
        driver = webdriver.Chrome(chrome_options=chrome_options)  # 启动浏览器并设置chrome_options参数

        driver.get('https://fanyi.baidu.com/?aldtype=85#en/zh/')
        try:driver.find_element_by_xpath('/html/body/div[1]/div[6]/div/div/div[2]/span').click()    # 取消广告
        except:continue
        translation = ''
        driver.get('https://fanyi.baidu.com/?aldtype=85#en/zh/'+oneword)
        driver.implicitly_wait(5)
        PhoneText = driver.find_elements_by_class_name('phonetic-transcription')
        res = ''
        for n,i in enumerate(PhoneText):
            phonecont = (i.text)
            taglength = 0
            try:
                if '英' in phonecont:
                    engph = re.sub('[\[\]ˌˈ]', ' ', phonecont.split('\r\n')[0].split(' ')[1]).lstrip().rstrip().replace('ː',':').replace('ɡ','g')  # ə kaʊntə bɪləti
                    tagmap = IPAdic
                else:
                    engph = re.sub('[\[\]ˌˈ]',' ',phonecont.split('\r\n')[1].split(' ')[1]).lstrip().rstrip().replace('ː',':').replace('ɡ','g')    # ə kaʊntə bɪləti
                    tagmap = KKdic
                switlst = []
                for n, i in enumerate(engph):
                    if n <= len(engph) - 2:
                        str = i + engph[n + 1]
                        if str in tagmap:
                            # print('Y',n,str,n+len(str)-1)
                            switlst.append('%s\t%s&%s' % (str, n, n + len(str) - 1))
                        else:
                            # print('N',n,i)
                            switlst.append('%s\t%s' % (i, n))
                    else:
                        # print('A',n,i)
                        switlst.append('%s\t%s' % (i, n))
                newlst, dic = [], {}
                for onestr in switlst:
                    value = onestr.split('\t')[0]
                    key = onestr.split('\t')[1]
                    if '&' in onestr:
                        dic[key.split('&')[0]] = value
                        dic[key.split('&')[1]] = ' '
                    else:
                        if key not in dic:
                            dic[key] = value
                taglength = (len([i for i in dic.values() if i != ' ']))
                sourcestr = ' '.join([i for i in dic.values() if i != ' '])
                resstr = ''
                for k, v in dic.items():
                    if v != ' ':
                        resstr += tagmap[v] + ' '
                res = resstr
            except:
                continue
            if taglength == len([i for i in resstr.split(' ') if i != '']):
                # print('目标单词\t%s\t【%s】\n百度音标：\t%s\n对应待插入音标如下：\n[vocabulary]\n%s/%s/\n'%(oneword,translation,phonecont,sourcestr,resstr.rstrip()))
                wres.write('目标单词\t%s\t【%s】\n百度音标：\t%s\n对应待插入音标如下：\n[vocabulary]\n%s/%s/\n\n'%(oneword,translation,phonecont,sourcestr,resstr.rstrip()))
                time.sleep(random.randint(2,4))
                phonecont, translation = '', ''
            else:wres.write('请检查单词：%s\n\n'%(oneword))











