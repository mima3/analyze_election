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
    parties = dom.xpath('//div[@class="snkH2Box"]/h2')
    tables = dom.xpath('//table[@class="snkTbl01"]')
    block = dom.xpath('//div[@class="BreadCrumb"]/h1')[0].text_content().encode('utf-8')
    block = block[block.find('：')+len('：'):]
    for i in range(0, len(parties)):
        h2 = parties[i].text_content().encode('utf-8')
        partyName = h2.split('\n')[0]
        members = tables[i].xpath('tbody/tr')
        for m in members:
            name = m.xpath('td[@class="namae"]')[0].text_content().encode('utf-8')
            lstNum = m.xpath('td[@class="lstNum"]')[0].text_content().encode('utf-8')
            age = m.xpath('td[@class="age"]')[0].text_content().encode('utf-8')
            status = m.xpath('td[@class="status"]')[0].text_content().encode('utf-8')
            net = m.xpath('td[@class="net"]/ul')[0]
            twitterEl = net.xpath('li[@id="twitter"]/a')
            facebookEl = net.xpath('li[@id="facebook"]/a')
            hpEl = net.xpath('li[@id="HomePage1"]/a')
            areaEl = m.xpath('td[@class="w"]/a')
            area = ''
            twitter = ''
            facebook = ''
            hp = ''
            if twitterEl:
                twitter = twitterEl[0].attrib['href'].encode('utf-8')
            if facebookEl:
                facebook = facebookEl[0].attrib['href'].encode('utf-8')
            if hpEl:
                hp = hpEl[0].attrib['href'].encode('utf-8')
            if areaEl:
                area =areaEl[0].text_content().encode('utf-8')
            print ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (block, partyName,lstNum, name, age, status, area, twitter, facebook, hp))

def main(argvs, argc):
    """
    このスクリプトでは、朝日新聞の情報から小選挙区の立候補者を取得します
    """
    for i in range(1, 12):
        url = ('http://www.asahi.com/senkyo/sousenkyo47/kouho/B%s.html' % str(i).zfill(2))
        print_area(url)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))