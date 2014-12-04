#!/usr/bin/python
# -*- coding: utf-8 -*-
from analyze_party_homepage import AnalyzePartyHomePage
import sys
import calc_distance
import graphviz_distance
import json


def main(argvs, argc):
    """
    このスクリプトでは、データベースに登録した内容を集計してJSONとPNGで出力します
    """
    if(argc != 5):
        print ("Usage #python %s dbname json_path png_path fontname" % argvs[0])
        print ('font path : ex "ms ui gothic" or "/home/fonts/ipca.ttc"')
        return -1
    dbname = argvs[1]
    json_path = argvs[2]
    png_path = argvs[3]
    font_path = argvs[4]

    ahp = AnalyzePartyHomePage(dbname)
    i = 0
    results = ahp.calc_tf_idf()
    keyword_count = 100
    report_data = []
    for ret in results.values():
        party_data = {
            'name' : ret.category,
            'words' : [],
            'info' : ahp.get_category_info(ret.category)
        }
        j = 1
        for k, v in sorted(ret.term_scores.items(), key=lambda x: x[1], reverse=True):
            wd_data = {
                'text' : k,
                'weight' : v
            }
            party_data['words'].append(wd_data)
            if j >= keyword_count:
                break
            j = j + 1
        i = i + 1

        report_data.append(party_data)

    distance_result = calc_distance.calc_distance(results)
    graphviz_distance.draw_distance(distance_result, png_path, font_path)

    f = open(json_path, 'w')
    f.write(json.dumps(report_data))
    f.close()

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))