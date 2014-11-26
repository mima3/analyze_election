#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from election_db import ElectionDb


def main(argvs, argc):
    """
    小選挙区情報CSVをインポートする
    """
    if(argc != 3):
        print "Usage #python %s dbname csv" % argvs[0]
        return -1

    dbname = argvs[1]
    path = argvs[2]
    db = ElectionDb(dbname)
    db.ImportElectionArea(path)
    print db.dbpath, " is imported."

    return 0

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
