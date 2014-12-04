#!/usr/bin/python
# -*- coding: utf-8 -*-
from analyze_party_homepage import AnalyzePartyHomePage
import json
import sys


def main(argvs, argc):
    """
    このスクリプトでHomePageの情報を記録するデータベースを作成します
    """
    if(argc != 3):
        print "Usage #python %s dbname party_json" % argvs[0]
        return -1
    dbname = argvs[1]
    party_json = argvs[2]
    ahp = AnalyzePartyHomePage(dbname)

    f = open(party_json, 'r')
    partys = json.load(f)
    f.close()

    #partys = {PartyInfo("自由民主党","https://special.jimin.jp/",["https://www.jimin.jp/"],["https://www.jimin.jp/activity/conference/weekly.html?wk=-100","https://www.jimin.jp/activity/conference/weekly.html?wk=100"])
    #                    ,PartyInfo("公明党","https://www.komei.or.jp/",[],[])
    #                    ,PartyInfo("民主党","http://dpj-voice.jp/",["http://www.dpj.or.jp/"],[""])
    #                    ,PartyInfo("日本維新の会","https://j-ishin.jp/",[],[])
    #                    ,PartyInfo("みんなの党","http://san2013.your-party.jp/",["http://www.your-party.jp/"],[])
    #                    ,PartyInfo("生活の党","http://www.seikatsu1.jp/",[],[])
    #                    ,PartyInfo("日本共産党","http://www.jcp.or.jp/",[],[])
    #                    ,PartyInfo("社民党","http://www5.sdp.or.jp/",[],[])
    #                 }

    for p in partys:
        print "============================="
        print (p['name'].encode('utf-8'))
        ahp.create_pages(p['name'], p['root_url'], p['positive_list'], p['exclude_filter'])
        for l in ahp.anlyze_url.results:
            print (l)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
