#!/usr/bin/python
# -*- coding: utf-8 -*-
from analyze_party_homepage import AnalyzePartyHomePage
import sys

def main(argvs, argc):
    """
    このスクリプトでは、データベース中のホームページの内容を単語単位に集計します
    """
    if(argc != 2):
        print "Usage #python %s dbname" % argvs[0]
        return -1
    ahp = AnalyzePartyHomePage(argvs[1])
    ahp.create_tokens()

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
