#!/usr/bin/python
# -*- coding: utf-8 -*-
from analyze_db import AnalyzeDb
from analyze_url import AnalyzeUrl
import lxml.html
import MeCab
import re
from collections import defaultdict
from math import log
import nltk
from tf_idf_result import tf_idf_result


class AnalyzePartyHomePage:
    def __init__(self, db_path):
        self.db = AnalyzeDb(db_path)
        self.anlyze_url = None
        self.category_id = 0
        self.mecab = MeCab.Tagger("")

    def __del__(self):
        self.db = None

    def add_page(self, url, raw):
        self.db.add_page(self.category_id, url, raw)

    def get_cache(self, url):
        return self.db.get_raw_data(url)

    def create_pages(self, category, root_url, positive_filter, exclude_filter, use_cache=True):
        """
        政党用のホームページの解析を行いDBに格納する
        @param category 政党名
        @param root_url 解析開始のURL
        @param positive_filter この配列で指定したURLで開始するページは解析対象
        @param exclude_filter この配列で指定したURLで開始するページは解析対象外
        @param use_cache Falseの場合、取得済みのページを削除して解析しなおす
        """
        if not use_cache:
            self.db.delete_category(category)

        self.category_id = self.db.get_category_id(category)
        if self.category_id is None:
            self.db.add_category(category, root_url)
            self.category_id = self.db.get_category_id(category)

        if self.category_id is None:
            return False

        self.anlyze_url = AnalyzeUrl(root_url, positive_filter, exclude_filter, self.add_page, self.get_cache)
        self.anlyze_url.analyze()
        return True

    def create_tokens(self):
        categories = self.db.get_categories()
        for id, category in categories.items():
            print category
            self.create_category_tokens(id, category)
        self.db.create_counting_tokens()

    def get_text_content(self, text):
        encodings = [
            "",
            '<?xml version="1.0" encoding="utf-8"?>',
            '<?xml version="1.0" encoding="Shift-Jis"?>',
            '<?xml version="1.0" encoding="euc-jp"?>',
        ]
        bestscore = -1
        bestenc = None
        ret = ""
        for enc in encodings:
            try:
                root = lxml.html.fromstring(enc + text)
                scripts = root.xpath('//script')
                for s in scripts:
                    s.getparent().remove(s)

                scripts = root.xpath('//style')
                for s in scripts:
                    s.getparent().remove(s)

                ret = root.text_content().encode('utf-8')
                return ret
            except UnicodeDecodeError, err:
                print "encode error %s" % (enc)
                pass
        return ""

    def create_category_tokens(self, category_id, category):
        url_list = self.db.get_category_url_list(category)
        i = 0
        for id, url in url_list.items():
            self.db.begin()
            if i % 10 == 0:
                print str(i) + "/" + str(len(url_list))
            self.db.delete_token(id)

            raw = self.db.get_raw_data(url)
            print url
            text = self.get_text_content(raw)
            node = self.mecab.parseToNode(text)
            while node:
                fs = node.feature.split(",")
                if fs[0] in ['形容詞', '形容動詞', '感動詞', '副詞', '連体詞', '名詞', '動詞']:
                    if fs[1] != '数':
                        self.db.add_token(id, node.surface)
                node = node.next
            self.db.commit()
            i = i + 1
        return True

    def calc_tf_idf(self):
        result = defaultdict(tf_idf_result)
        tokens_count_by_category = self.db.get_tokens_count_group_by_category()
        tokens_counting = self.db.get_tokens_counting()
        for category, surfaces in tokens_counting.items():
            for s, l in surfaces.items():
                # 特定文章における用語の重要度
                # l[0] カテゴリ中にsが出現する頻度 / カテゴリ中の総単語数
                tf = float(l[0]) / float(tokens_count_by_category[category])

                # log(総文章数/単語のある文章数)
                # l[1] 該当文字が含まれるカテゴリの数
                idf = 1.0
                try:
                    idf = 1.0 + log(float(len(tokens_count_by_category.keys())) / float(l[1]))
                except ZeroDivisionError:
                    pass

                if not category in result:
                    result[category] = tf_idf_result(category)
                result[category].set_score(s, tf * idf)

        return result

    def get_category_info(self, category):
        return self.db.get_category_info(category)

    def calc_distance(self, tf_idf_ret):
        """
        tf_idf のスコアを元に距離を取得します。
        ret[str] = float
        """
        result = defaultdict(dict)
        for fromCategory, fromTokens in tf_idf_ret.items():
            for toCategory, toTokens in tf_idf_ret.items():
                if fromCategory == toCategory:
                    continue

                for f in fromTokens.term_scores:
                    if f not in toTokens.term_scores:
                        toTokens.set_score(f, 0)

                for t in toTokens.term_scores:
                    if t not in fromTokens.term_scores:
                        fromTokens.set_score(t, 0)

                v1 = [score for (term, score) in sorted(fromTokens.term_scores.items())]
                v2 = [score for (term, score) in sorted(toTokens.term_scores.items())]
                result[fromCategory][toCategory] = nltk.cluster.util.cosine_distance(v1, v2)
        return result
