#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import sys
import os
from lxml import etree
from rdp import rdp
from sympy.geometry import Point, Polygon
import pickle
import time
import csv

class ElectionDb:
    """
    選挙情報を管理するデーターベース
    """
    def __init__(self, dbpath):
        self._dbpath = dbpath
        self._conn = sqlite3.connect(dbpath)
        self._conn.text_factory = str

    def __del__(self):
        if self._conn:
            self.close()

    def close(self):
        self._conn.close()
        self._conn = None

    @property
    def dbpath(self):
        return self._dbpath

    def create_db(self):
        """
        テーブルを作成する
        """
        sql = '''CREATE TABLE IF NOT EXISTS administrative_boundary(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 gml_id TEXT UNIQUE,
                                 bounds TEXT,
                                 prefecture_name TEXT,
                                 sub_prefecture_name TEXT,
                                 county_name TEXT,
                                 city_name TEXT,
                                 area_code TEXT);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS administrative_boundary_index ON  administrative_boundary(gml_id);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS administrative_boundary_prefecture_name_index ON  administrative_boundary(prefecture_name);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS administrative_boundary_city_name_index ON  administrative_boundary(prefecture_name,city_name);'''
        self._conn.execute(sql)

        sql = '''CREATE TABLE IF NOT EXISTS surface(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 surface_id TEXT ,
                                 curve_member TEXT);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS surface_index ON  surface(surface_id,curve_member);'''
        self._conn.execute(sql)

        sql = '''CREATE TABLE IF NOT EXISTS curve(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 curve_id TEXT,
                                 lat NUMBER,
                                 lng NUMBER);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS curve_index ON  curve(curve_id);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS curve_lat_index ON  curve(lat);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS curve_lng_index ON  curve(lng);'''
        self._conn.execute(sql)

        sql = '''CREATE TABLE IF NOT EXISTS polygon(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 curve_id TEXT,
                                 object BLOB);'''
        self._conn.execute(sql)

        sql = '''CREATE INDEX IF NOT EXISTS polygon_index ON  curve(curve_id);'''
        self._conn.execute(sql)

        sql = '''CREATE TABLE IF NOT EXISTS election_area(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 key TEXT,
                                 prefecture_name TEXT,
                                 sub_prefecture_name TEXT,
                                 county_name TEXT,
                                 city_name TEXT,
                                 notes TEXT);'''
        self._conn.execute(sql)


    def ImportAdministrativeBoundary(self, xml):
        f = None
        contents = None
        namespaces = {
            'ksj': 'http://nlftp.mlit.go.jp/ksj/schemas/ksj-app',
            'gml': 'http://www.opengis.net/gml/3.2',
            'xlink': 'http://www.w3.org/1999/xlink',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
        self._conn.execute('begin')

        print ('admins....')
        context = etree.iterparse(xml, events=('end',), tag='{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}AdministrativeBoundary')
        for event, admin in context:
            adminId = admin.get('{http://www.opengis.net/gml/3.2}id')
            print (adminId)
            bounds = admin.find('ksj:bounds', namespaces=namespaces).get('{http://www.w3.org/1999/xlink}href')[1:]
            prefectureName = admin.find('ksj:prefectureName', namespaces=namespaces).text
            subPrefectureName = admin.find('ksj:subPrefectureName', namespaces=namespaces).text
            countyName = admin.find('ksj:countyName', namespaces=namespaces).text
            cityName = admin.find('ksj:cityName', namespaces=namespaces).text
            areaCode = admin.find('ksj:administrativeAreaCode', namespaces=namespaces).text
            sql = '''INSERT INTO administrative_boundary
                     (gml_id, bounds, prefecture_name, sub_prefecture_name, county_name, city_name, area_code)
                     VALUES(?, ?, ?, ?, ?, ?, ?);'''
            self._conn.execute(sql, [adminId, bounds, prefectureName, subPrefectureName, countyName, cityName, areaCode ])

            admin.clear()
            # Also eliminate now-empty references from the root node to <Title> 
            while admin.getprevious() is not None:
                del admin.getparent()[0]
        del context

        print ('surfaces....')
        context = etree.iterparse(xml, events=('end',), tag='{http://www.opengis.net/gml/3.2}Surface')
        for event, surf in context:
            surfId = surf.get('{http://www.opengis.net/gml/3.2}id')
            print (surfId)
            curveMembers = surf.xpath('.//gml:curveMember', namespaces=namespaces)
            for member in curveMembers:
                memberId = member.get('{http://www.w3.org/1999/xlink}href')[1:]
                sql = '''INSERT INTO surface
                         (surface_id, curve_member)
                         VALUES(?, ?);'''
                self._conn.execute(sql, [surfId, memberId ])
            surf.clear()
            # Also eliminate now-empty references from the root node to <Title> 
            while surf.getprevious() is not None:
                del surf.getparent()[0]
        del context


        print ('curves....')
        context = etree.iterparse(xml, events=('end',), tag='{http://www.opengis.net/gml/3.2}Curve')
        for event, curve in context:
            curveId = curve.get('{http://www.opengis.net/gml/3.2}id')
            posLists = curve.xpath('.//gml:posList', namespaces=namespaces)
            print (curveId)
            for posList in posLists:
                poly = []
                points = posList.text.split("\n")
                for point in points:
                    pt = point.replace("\t", '').split(' ')
                    if len(pt) != 2:
                      continue
                    poly.append([float(pt[0]), float(pt[1])])
                polyRdp = poly # rdp(poly, epsilon=0.001)
                for pt in polyRdp:
                  lat = pt[0]
                  lng = pt[1]
                  sql = '''INSERT INTO curve
                           (curve_id, lat, lng)
                         VALUES(?, ?, ?);'''
                  self._conn.execute(sql, [curveId, lat, lng ])
            curve.clear()
            # Also eliminate now-empty references from the root node to <Title> 
            while curve.getprevious() is not None:
                del curve.getparent()[0]
        del context

        self.Commit()

    def GetPrefecture(self):
        """
        県の一覧取得
        """
        sql = '''select 
                   distinct 
                   prefecture_name
                 from 
                   administrative_boundary order by id;'''
        rows = self._conn.execute(sql)
        res = []
        for r in rows:
            res.append(r[0])
        return res

    def GetCityGeo(self, prefectureName, subPrefectureName='', countyName='', cityName=''):
        sql = '''select 
                   a.prefecture_name , 
                   a.sub_prefecture_name ,
                   a.county_name,
                   a.city_name,
                   a.bounds,
                   b.curve_member,
                   c.lat,
                   c.lng
                 from 
                   administrative_boundary as a 
                   inner join surface as b on b.surface_id = a.bounds
                   inner join curve as c on b.curve_member = c.curve_id
                 where a.prefecture_name = ? '''
        param = [prefectureName]

        if (len(subPrefectureName) > 0):
          param.append(subPrefectureName);
          sql = sql + 'and a.sub_prefecture_name = ?'

        if (len(countyName) > 0):
          param.append(countyName);
          sql = sql + 'and a.county_name = ?'

        if (len(cityName) > 0):
          param.append(cityName);
          sql = sql + 'and a.city_name = ?'

        rows = self._conn.execute(sql, param)
        return rows

    def GetElectionArea(self, prefectureName, subPrefectureName='', countyName='', cityName=''):
        """
        選挙区の取得
        """
        sql = '''select 
                   key , 
                   notes
                 from 
                   election_area 
                 where 
                   (prefecture_name = ?) AND
                   (sub_prefecture_name = '' OR prefecture_name = ?) AND
                   (county_name = '' OR county_name = ?) AND
                   (city_name= '' OR city_name = ?)'''
        rows = self._conn.execute(sql, [prefectureName, subPrefectureName, countyName, cityName ])
        return rows

    def GetElectionAreaInformation(self, electionArea):
        """
        選挙区の詳細情報取得
        """
        sql = '''select 
                   key , 
                   notes ,
                   prefecture_name,
                   sub_prefecture_name, 
                   county_name,
                   city_name
                 from 
                   election_area 
                 where 
                   key = ?'''
        rows = self._conn.execute(sql, [electionArea ])
        return rows

    def GetPrefectureElectionArea(self, prefectureName):
        sql = '''select distinct
                   key 
                 from 
                   election_area 
                 where 
                   (prefecture_name = ?) 
                 order by id;'''
        rows = self._conn.execute(sql, [prefectureName ])
        return rows

    def ConvertPoly(self):
        """
        curveテーブルからpolygonの作成
        """
        self._conn.execute('begin')
        sql = '''DELETE FROM polygon'''
        self._conn.execute(sql)

        sql = '''select curve_id,lat,lng from curve  order by curve_id'''
        rows = self._conn.execute(sql)
        dict = {}
        for r in rows:
            key = r[0]
            if dict.get(key) is None:
                dict[key] = []
            dict[key].append((r[1], r[2]))

        for key in dict:
            print (key)
            poly = Polygon(*dict[key])
            obj = pickle.dumps(poly)
            sql = '''INSERT INTO polygon
                           (curve_id, object)
                         VALUES(?, ?);'''
            self._conn.execute(sql, [key, obj ])
        self.Commit()

    def GetPos(self, lat, long):
        """
        現在の経度緯度に紐づくcurveのデータを取得
        """
        m =0.005
        while 1:
            rows = self._getCurveId(lat, long, m).fetchall()
            if rows:
              break
            m = m * 2
            if m > 0.1:
              return None

        dict = {}
        pt = Point(lat, long)

        for r in rows:
            key = r[0]
            ret = self._isCrossCurveId(pt, key)
            if ret:
                return ret
        return None

    def _getCurveId(self, lat, long, m):
        sql = '''select distinct
                   curve_id
                 from 
                   curve
                 where
                   lat between ? and ? and lng between ? and ?'''
        rows = self._conn.execute(sql, [lat-m, lat+m ,long-m ,long+m])
        return rows

    def _isCrossCurveId(self, pt, curveId):
        sql = '''select        
                   a.prefecture_name , 
                   a.sub_prefecture_name ,
                   a.county_name,
                   a.city_name,
                   c.object
                 from 
                   polygon as c
                   inner join surface as b  on b.curve_member = c.curve_id
                   inner join administrative_boundary as a on b.surface_id = a.bounds
                 where
                   c.curve_id = ?'''
        rows = self._conn.execute(sql, [curveId])
        for r in rows:
            poly = pickle.loads(r[4])
            if hasattr( poly, 'encloses_point' ):
                if poly.encloses_point(pt):
                    res = {
                        'prefectureName': r[0], 
                        'subPrefectureName': r[1],
                        'countyName' : r[2],
                        'cityName': r[3]
                    }
                    return res

    def ImportElectionArea(self, path):
        """
        小選挙区の地区情報のCSVの取り込み
        """
        reader = csv.reader(open(path,'rb'))
        self._conn.execute('begin')

        sql = '''DELETE FROM election_area'''
        self._conn.execute(sql)

        for row in reader:
            sql = '''INSERT INTO election_area
                     (key,  prefecture_name, sub_prefecture_name, county_name, city_name, notes)
                     VALUES(?, ?, ?, ?, ?, ?);'''
            self._conn.execute(sql, [unicode(row[0],'cp932'), unicode(row[1],'cp932'),unicode(row[2],'cp932'),unicode(row[3],'cp932'),unicode(row[4],'cp932'),unicode(row[5],'cp932') ])

        self.Commit()

    def Commit(self):
        self._conn.commit()

    def Rollback(self):
        self._conn.rollback()
