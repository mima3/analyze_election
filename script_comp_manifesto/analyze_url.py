#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib2
import lxml.html
import re
import os.path
import urlparse
import socket


class AnalyzeUrl:
    def __init__(self, url, positive_filter=[], exclude_filter=[], func_get_contents=None, func_get_cache=None):
        self.url = url
        self.positive_filter = positive_filter
        self.exclude_filter = exclude_filter

        base_url = self.get_base_url(url)
        if base_url not in self.positive_filter:
            self.positive_filter.append(base_url)
        self.results = []
        self.func_get_contents = func_get_contents
        self.func_get_cache = func_get_cache
        self.same_url_count = 0

    def get_base_url(self, url):
        root, ext = os.path.splitext(url)
        base_url = url
        if ext:
            base_url = os.path.dirname(url)
        if base_url[-1:] != "/":
            base_url = base_url + "/"
        return base_url

    def check_filter(self, url):
        for f in self.exclude_filter:
            if re.match('^' + f, url):
                return False

        for f in self.positive_filter:
            if re.match('^' + f, url):
                return True
        return False

    def get_links(self, url, score="*"):
        try:
            url = url.encode('utf-8')
        except:
            print "URL%s can not encode" % (url)
            pass
        url = url.strip()
        root, ext = os.path.splitext(url)
        print ext
        exclude_ext = [
            ".jpg",
            ".JPG",
            ".png",
            ".PNG",
            ".gif",
            ".GIF",
            ".pdf",
            ".PDF",
            ".xls",
            ".XLS",
            ".doc",
            ".DOC",
            ".zip"
        ]
        if ext in exclude_ext:
            print ("Skip extention.%s" % (url))
            return False
        html = None
        if self.func_get_cache:
            html = self.func_get_cache(url)
        if html is None:
            try:
                print ("%s Req:%s" % (score, url))
                r = urllib2.urlopen(url, timeout=30)
                headers = r.info()
                url = r.geturl()
                content_type = headers.getheaders("Content-Type")
                if re.match('^text/html', content_type[0]) is None:
                    print ("get_link(%s) is not text/html :Content-Type %s" % (url, content_type))
                    return False
                html = r.read()
                if self.func_get_contents:
                    self.func_get_contents(url, html)

            except urllib2.HTTPError, e:
                print ("get_link(%s) URL HTTPError %s" % (url, str(e.reason)))
                return False
            except ValueError, e:
                print ("get_link(%s) URL ValueError %s" % (url, str(e)))
                return False
            except urllib2.URLError, e:
                print ("get_link(%s) URL Error %s" % (url, str(e.reason)))
                return False
            except socket.timeout, e:
                print ("timeout %s" % (url))
                return False
            except:
                print ("unexpected %s" % (url))
                return False
        else:
            print ("%s Cache:%s" % (score, url))

        try:
            root = lxml.html.fromstring(html)
        except:
            print ("unexpected html %s" % (url))
            return False

        contents = root.xpath('//a')
        for c in contents:
            if 'href' in c.attrib:
                href = re.split("#", c.attrib['href'])[0]
                href = href.strip()
                try:
                    href = href.encode('utf-8')
                except:
                    print "href %s can not encode" % (href)
                    continue

                if re.match('^[http|https]', href) is None:
                    # URLがないので相対パス
                    href = urlparse.urljoin(url, href)
                if href not in self.results:
                    if self.check_filter(href):
                        self.results.append(href)
                        self.get_links(href, score + "*")
        return True

    def analyze(self):
        sys.setrecursionlimit(3000)
        self.results = []
        self.get_links(self.url)
        sys.setrecursionlimit(1000)
