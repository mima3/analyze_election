#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from election_db import ElectionDb


def main(argvs, argc):
    """
    国土数値情報　行政区域データをDBにインポートする
    http://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03.html
    """
    if(argc != 3):
        print "Usage #python %s dbname xml" % argvs[0]
        return -1

    dbname = argvs[1]
    xml = argvs[2]
    db = ElectionDb(dbname)
    db.ImportAdministrativeBoundary(xml)
    print db.dbpath, " is imported."

    return 0

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
