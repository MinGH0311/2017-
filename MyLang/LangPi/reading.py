#-*- encoding:utf-8 -*-

import urllib2
import BeautifulSoup
from Reading import Translate_Google_without_API
from Reading import Translate_Naver
from Reading import DOC_comp
import math

def Translate(string, src, dst, select = "Google"):
    if select == "Google":
        result = Translate_Google_without_API.translate(string, src, dst)
    elif select == "Naver":
        result = Translate_Naver.translate(string, src, dst)
    return result

def Translate_from_URL(url, src, dst, select = "Google"):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    res = []
    if 'cnn' in url:
        div = soup.findAll('div', attrs={'id':'storytext'})
        # print div
        soup = BeautifulSoup.BeautifulSoup(str(div))
        div = soup.findAll('p')
        for txt in div:
            res.append(txt.text)

def read(string='', user_answer='', lang='en'):
    answer = []
    answer.append(unicode(Translate(string, lang, 'ko')))
    tmp = Translate(string, lang, 'ja').replace(u'', ' ')
    answer.append(unicode(Translate(tmp, 'ja', 'ko')))
    return str(int(math.log(DOC_comp.comp_bleu(answer, unicode(user_answer))*100+0.5, 100)*100))+'%'
    # print str(int((math.log(int(DOC_comp.comp_bleu(answer, unicode(user_answer))*100), 8)+(1-math.log(100, 8)))*100))+'%'

