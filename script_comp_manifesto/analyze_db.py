#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import datetime
import time
import re
import lxml.html
from collections import defaultdict


class AnalyzeDb:
    def __init__(self, path):
        self._conn = sqlite3.connect(path)
        self._conn.text_factory = str
        self.setup()

    def setup(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories (category TEXT, id INTEGER PRIMARY KEY, url TEXT);'''
        self._conn.execute(sql)

        sql = '''CREATE TABLE IF NOT EXISTS counting_tokens (category_id NUMERIC, cnt NUMERIC, surface TEXT);'''
        self._conn.execute(sql)

        sql = '''CREATE TABLE IF NOT EXISTS pages (category_id NUMERIC, last_update TEXT, id INTEGER PRIMARY KEY, raw TEXT, url TEXT);'''
        self._conn.execute(sql)

        sql = '''CREATE TABLE IF NOT EXISTS tokens (page_id NUMERIC, surface TEXT);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS categories_index_url ON categories(category ASC);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS counting_tokens_index_category_id ON counting_tokens(category_id ASC);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS counting_tokens_index_surface ON counting_tokens(surface ASC);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS pages_index_category_id ON pages(category_id ASC);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS pages_index_url ON pages(url ASC);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS tokens_index_page_id ON tokens(page_id ASC);'''
        self._conn.execute(sql)

    def __del__(self):
        self._conn.close()

    def add_category(self, category, url):
        """
        カテゴリーの追加
        @param[in] category カテゴリー名
        @param[in] url            URL
        """
        sql = "delete from categories where category=?"
        self._conn.execute(sql, [category, ])

        sql = "insert into categories (category,url) values(?,?)"
        self._conn.execute(sql, [category, url, ])
        self._conn.commit()

    def add_page(self, category_id, url, raw):
        """
        ページの追加
        @param[in] category カテゴリー名
        @param[in] url            URL
        @param[in] raw            コンテンツの内容
        """
        sql = "delete from pages where url=?"
        self._conn.execute(sql, [url, ])

        sql = "insert into pages (category_id,url,raw,last_update) values(?,?,?,?)"
        self._conn.execute(sql, [category_id, url, raw, datetime.datetime.now(), ])
        self._conn.commit()

    def delete_category(self, category):
        """
        カテゴリーの削除
        @param[in] category カテゴリー名
        """
        id = self.get_category_id(category)
        if id is None:
            return

        sql = "delete from tokens where page_id in (select pages.id from pages inner join categories on categories.id = pages.category_id where categories.category = ?)"
        self._conn.execute(sql, [category, ])

        sql = "delete from pages where category_id=?"
        self._conn.execute(sql, [id, ])

        sql = "delete from categories where category=?"
        self._conn.execute(sql, [category, ])

        self._conn.commit()

    def get_category_id(self, category):
        """
        カテゴリーのIDの取得
        @param[in] category カテゴリー名
        @return カテゴリーIDの取得。Noneの場合は該当カテゴリーはない
        """
        sql = "select id from categories where category = ?"
        rows = self._conn.execute(sql, [category, ])
        for r in rows:
            return r[0]
        return None

    def get_raw_data(self, url):
        sql = "select raw from pages where url = ?"
        rows = self._conn.execute(sql, [url, ])
        for r in rows:
            return r[0]
        return None

    def get_page_id(self, url):
        """
        URLのIDの取得
        @param[in] url page
        @return カテゴリーIDの取得。Noneの場合は該当カテゴリーはない
        """
        sql = "select id from pages where url = ?"
        rows = self._conn.execute(sql, [url, ])
        for r in rows:
            return r[0]
        return None

    def get_categories(self):
        sql = "select id, category from categories"
        result = {}
        rows = self._conn.execute(sql)
        for r in rows:
            result[r[0]] = r[1]
        return result

    def get_category_info(self, category):
        sql = 'select max(last_update), min(last_update), count(*) from pages inner join categories on categories.id= pages.category_id where categories.category = ?;'
        rows = self._conn.execute(sql, [category, ])
        for r in rows:
            ret = {
                'max' : r[0],
                'min' : r[1],
                'count' : r[2]
            }
            return ret
        return None

    def get_category_url_list(self, category):
        sql = "select pages.id,pages.url from pages inner join categories on categories.id = pages.category_id where categories.category = ?"
        result = {}
        rows = self._conn.execute(sql, [category, ])
        for r in rows:
            result[r[0]] = r[1]
        return result

    def delete_token(self, page_id):
        sql = "delete from tokens where page_id=?"
        self._conn.execute(sql, [page_id, ])

    def add_token(self, page_id, surface):
        """
        ページの追加
        @param[in] category カテゴリー名
        @param[in] url            URL
        @param[in] raw            コンテンツの内容
        """
        sql = "insert into tokens (page_id,surface) values(?,?)"
        self._conn.execute(sql, [page_id, surface, ])

    def create_counting_tokens(self):
        """
        tokensテーブルより集計を行いcounting_tokensテーブルを作成する
        これはcategory_idとsurfaceでグループ化して、該当のカテゴリーにその単語が何回登場したかを記述する
        """
        self._conn.execute("delete from counting_tokens")
        self._conn.execute("insert into counting_tokens ( category_id, surface, cnt ) select pages.category_id,surface,count(*) cnt    from tokens inner join pages on pages.id = tokens.page_id    where category_id group by surface,pages.category_id")
        self._conn.commit()

    def get_tokens_count_group_by_category(self):
        """
        カテゴリーに分類されたトークンの数を取得
        @return カテゴリーID：トークン数のディクショナリ
        """
        rows = self._conn.execute("select categories.category, sum(cnt) from counting_tokens inner join categories on categories.id = counting_tokens.category_id group by category_id")
        result = {}
        for r in rows:
            result[r[0]] = r[1]
        return result

    def get_tokens_counting(self):
        rows = self._conn.execute("select categories.category, counting_tokens.surface,counting_tokens.cnt, grp.num_texts_with_term from counting_tokens inner join    ( select surface ,count(*) as num_texts_with_term from counting_tokens group by surface ) as grp on counting_tokens.surface = grp.surface inner join categories on categories.id = counting_tokens.category_id ")
        result = defaultdict(dict)
        for r in rows:
            if not r[0] in result:
                # カテゴリが未登録
                result[r[0]] = defaultdict(list)
            result[r[0]][r[1]] = [r[2], r[3]]
        return result

    def commit(self):
        self._conn.commit()

    def begin(self):
        self._conn.execute("BEGIN")
