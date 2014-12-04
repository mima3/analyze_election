#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib2
import lxml.html
import re
import os.path
import urlparse

def print_area(url):
    r = urllib2.urlopen(url, timeout=30)
    html = r.read()
    dom = lxml.html.fromstring(html)
    areas = dom.xpath('//div[@class="H2Box snkH2Box"]/h2')
    tables = dom.xpath('//table[@class="snkTbl01"]')
    for i in range(0, len(areas)):
        h2 = areas[i].text_content().encode('utf-8')
        areaName = h2.split('\n')[0]
        members = tables[i].xpath('tbody/tr')
        for m in members:
            name = m.xpath('td[@class="namae"]')[0].text_content().encode('utf-8')
            age = m.xpath('td[@class="age"]')[0].text_content().encode('utf-8')
            party = m.xpath('td[@class="party"]')[0].text_content().encode('utf-8')
            status = m.xpath('td[@class="status"]')[0].text_content().encode('utf-8')
            print ('%s,%s,%s,%s,%s' % (areaName, name, age, party, status))


def main(argvs, argc):
    """
    このスクリプトでは、朝日新聞の情報から小選挙区の立候補者を取得します
    """
    url = 'http://www.asahi.com/senkyo/sousenkyo46/kouho/A01.html'
    for i in range(1, 48):
        url = ('http://www.asahi.com/senkyo/sousenkyo46/kouho/A%s.html' % str(i).zfill(2))
        print_area(url)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))