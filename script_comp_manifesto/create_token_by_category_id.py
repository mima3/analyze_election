#!/usr/bin/python
# -*- coding: utf-8 -*-
from analyze_party_homepage import AnalyzePartyHomePage
import sys

category_id = int(sys.argv[1])
dbname = "analyze_hp.sqlite"

ahp = AnalyzePartyHomePage(dbname)
categories = ahp.db.get_categories()
print (categorys[category_id])
ahp.create_category_tokens(category_id, categories[category_id])
ahp.db.create_counting_tokens()
