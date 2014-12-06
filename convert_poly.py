#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from election_db import ElectionDb


def main(argvs, argc):
    """
    このスクリプトでcurveテーブルからpolygonの作成を行います。
    あらかじめ、polygonを作成しておくことで処理の高速化を狙います。
    """
    if(argc != 2):
        print "Usage #python %s dbname" % argvs[0]
        return -1

    dbname = argvs[1]
    db = ElectionDb(dbname)
    db.create_db()
    db.ConvertPoly()
    print db.dbpath, " is created."

    return 0

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
