# coding: utf-8
import sys
from niconico_ctrl import NicoCtrl
import json
from collections import defaultdict
import math
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = codecs.getwriter('utf-8') (sys.stdout)
import MeCab

def morph(mecab, wordcount, text):
    pos = [
      u'名詞',
      u'形容詞',
      u'形容動詞',
      u'感動詞',
      u'動詞',
      u'副詞'
    ]

    exclude=[
      u'8',
      u'８',
      u'w',
      u'ｗ',
      u'さん',
      u'ある',
      u'する',
      u'いる',
      u'やる',
      u'これ',
      u'それ',
      u'あれ',
      u'こと',
      u'の',
      u'そこ',
      u'ん',
      u'なる'
    ]

    node = mecab.parseToNode(text)
    while node:
        fs = node.feature.split(",")
        if fs[0] in pos:
            word = (fs[6] != '*' and fs[6] or node.surface)
            word = word.strip()
            if word.isdigit() == False:
                if len(word)!=1:
                    if word not in exclude:
                        wordcount[word] += 1
        node = node.next
    return wordcount

def main(argvs, argc):

    if len(argvs) != 2:
        print ('python analyze_nico_json.py xxxxx.json')
        return 1
    nico_json = argvs[1]
    f = open(nico_json, 'r')
    nico_json_data = json.load(f)

    p = ""
    #if dicdir == "":
    #  p = "-u%s" % (usrdicdir)
    #else:
    #  p = " -d%s -u%s" % (dicdir ,usrdicdir)
    mecab = MeCab.Tagger(p)

    wordcount = defaultdict(int)
    usercount = defaultdict(int)
    vpos_max = 0
    vpos_minute = 100 * 60
    vpos_div = vpos_minute * 1
    for data in nico_json_data:
        if vpos_max < data['vpos']:
            vpos_max = int(data['vpos'])

    vpos_list = []

    for i in xrange((vpos_max / vpos_div)+1):
        vpos_list.append({'maxtime': (i + 1) * vpos_div, 'count': 0})

    for data in nico_json_data:
        morph(mecab, wordcount, data['content'].encode('utf-8'))
        usercount[data['user_id']] += 1
        for i in reversed(xrange(len(vpos_list))):
            if vpos_list[i]['maxtime'] >= int(data['vpos']) and \
               (i==0 or (vpos_list[i-1]['maxtime'] < int(data['vpos']))):
                vpos_list[i]['count']  += 1
                break
    f.close()

    print ('Terms ###################################')
    termstats = []
    max=0
    for k, v in sorted(wordcount.items(), key=lambda x:x[1], reverse=True):
        if v > max:
            max = v

    for k, v in sorted(wordcount.items(), key=lambda x:x[1], reverse=True):
        if v == 1 and max > 1:
            break
        termstats.append( {"text" : k, "weight" : v} )
        print ('%s\t%d' % (k, v))
    f = open('term_' + nico_json, 'w')
    f.write(json.dumps(termstats))
    f.close()

    print ('Users ###################################')
    userstats = []
    max=0
    for k, v in sorted(usercount.items(), key=lambda x:x[1], reverse=True):
        if v > max:
            max = v

    for k, v in sorted(usercount.items(), key=lambda x:x[1], reverse=True):
        if v == 1 and max > 1:
            break
        userstats.append( {"text" : k, "weight" : v} )
        print ('%s\t%d' % (k, v))
    f = open('user_' + nico_json, 'w')
    f.write(json.dumps(userstats))
    f.close()

    print ('vpos ###################################')
    for i in xrange(len(vpos_list)):
        print ('%d\t%d' % ((vpos_list[i]['maxtime'] / vpos_minute) , vpos_list[i]['count']))
    f = open('vpos_' + nico_json, 'w')
    f.write(json.dumps(vpos_list))
    f.close()

    return 0

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
