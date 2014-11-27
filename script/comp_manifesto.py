#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MeCab
import nltk
from pdf_to_text import http_pdf_to_text
import calc_distance
import graphviz_distance

import urllib2
import lxml.html
import codecs
import datetime
import time
import sys
from collections import defaultdict
from tf_idf_result import tf_idf_result

mecab = MeCab.Tagger("")


class tf_idf_result:
    """
    tf-idfのスコアの結果を格納する
    """
    def __init__(self, doc):
        self.text = ''.join(doc)
        self.term_scores = defaultdict(int)

    def set_score(self, term, score):
        self.term_scores[term] = score


def get_tokens(text):
    """
    テキストから単語のリストを取得する
    text:UTF-8の文章
    return 単語のリスト
    """
    text = text.strip()
    text = text.replace('　', '')
    node = mecab.parseToNode(text)
    words = []
    pos = [u'形容詞', u'形容動詞', u'感動詞', u'副詞', u'連体詞', u'名詞', u'動詞']
    exclude = [
        u'・・・・・・・・・・・・・・・・・・・・・・・・・',
        u'，',
        u'１',
        u'２',
        u'３',
        u'４',
        u'５',
        u'６',
        u'７',
        u'８',
        u'９',
        u'０',
        u'さん',
        u'する',
        u'いる',
        u'やる',
        u'これ',
        u'それ',
        u'あれ',
        u'こと',
        u'の',
        u'そこ',
        u'なる',
        u'ない',
        u'ある'
    ]

    while node:
        fs = node.feature.split(",")
        if fs[0] in pos:
            word = (fs[6] != '*' and fs[6] or node.surface)
            if not word.isdigit():
                if len(word) > 0:
                    if word not in exclude:
                        words.append(word)
        node = node.next
    return words


def get_party_content(name, url):
    pdftotext_path = r"pdftotext"
    text, ret = http_pdf_to_text(url, pdftotext_path, '.')
    if not ret:
        print ("(%s)のURL(%s)からPDFの取得ができませんでした (%s)"
               % (name, url, text))
        return None
    return text

partys = {
    "自民党": "http://jimin.ncss.nifty.com/pdf/news/policy/126585_1.pdf",
    #"公明党": "https://www.komei.or.jp/policy/policy/pdf/manifesto2013.pdf",
    "民主党": "http://www.dpj.or.jp/global/downloads/manifesto2014.pdf",
    "維新の党": "https://ishinnotoh.jp/activity/news/2014/11/23/20141122-seisaku.pdf",
    #"次世代の党": "http://jisedai.jp/cp-bin/wordpress/wp-content/uploads/2014/11/%EF%BC%88%E6%94%BF%E7%AD%96%E9%9B%86%EF%BC%89%E6%AC%A1%E4%B8%96%E4%BB%A3%E3%81%8C%E8%AA%87%E3%82%8A%E3%82%92%E6%8C%81%E3%81%A6%E3%82%8B%E6%97%A5%E6%9C%AC%E3%82%92.pdf",
    #"共産党": "http://www.jcp.or.jp/web_download/seisaku/201307_seisaku_panf.pdf",
    "生活の党": "http://www.seikatsu1.jp/wp-content/uploads/0c4778a35f0cfe0a34fd3085e210a5c4.pdf"
    #"社民党": "http://www5.sdp.or.jp/policy/policy/election/2013/data/digest.pdf",
    #"みどりの風": "http://mikaze.jp/news/upload/1372851421_1.pdf"
}

docs = []
effective_partys = []
for k, v in partys.items():
    print (u"%sを処理中..." % (k))
    text = get_party_content(k, v)
    if text is None:
        continue
    docs.append(get_tokens(text))
    effective_partys.append(k)

results = {}
col = nltk.TextCollection(docs)

# tf    : Term Frequency 単語出現頻度     文章jにおける単語iの出現回数/全文章で出現する総単語数
# idf : Inverse Document Frequency        逆文章頻度 log(総ドキュメント数/単語iを含むドキュメント数）
# tf-idf : tf * idf
i = 0
for doc in docs:
    ret = tf_idf_result(doc)
    terms = list(set(doc))
    for term in terms:
        ret.set_score(term, col.tf_idf(term, doc))
    results[effective_partys[i]] = ret
    i = i + 1

i = 0
keyword_count = 100
print results
for key in results.keys():
    ret = results[key]
    print ("(%s)の上位%d位キーワード" % (key, keyword_count))
    j = 1
    for k, v in sorted(ret.term_scores.items(), key=lambda x: x[1], reverse=True):
        print ("%s	%f" % (k, v))
        if j >= keyword_count:
            break
        j = j + 1
    i = i + 1

distance_result = calc_distance.calc_distance(results)
graphviz_distance.draw_distance(distance_result, 'election_tfidf_reslut.png')