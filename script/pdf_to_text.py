# -*- coding: utf-8 -*-
import os
import re
import urllib2
import uuid
import subprocess


def http_pdf_to_text(url, pdftotext_path, tmp_folder):
    """
    HTTP経由でpdf_to_textを用いてPDFからTEXTを取得する
    @param url                        取得元のURL
    @param pdftotext_path pdftotextの絶対パス
    @param tmp_folder         一時ファイルを格納するフォルダ
    @retval 正常終了時は変換したテキスト。エラーの場合はエラーの内容。
    @retval True 正常終了 False 異常終了
    """
    tmp_uuid = str(uuid.uuid4())
    tmp_pdf_path = tmp_folder + "/" + tmp_uuid + ".pdf"
    tmp_txt_path = tmp_folder + "/" + tmp_uuid + ".txt"

    # http経由でPDFを取得
    try:
        r = urllib2.urlopen(url)
        html = r.read()
    except urllib2.HTTPError, e:
        return "HTTP Error code : " + str(e.code), False
    except urllib2.URLError, e:
        return "URL Error : " + str(e.reason), False

    # pdf をファイルに保存
    f = None
    try:
        f = open(tmp_pdf_path, "wb")
        f.write(html)
    except IOError, (errno, strerror):
        return "writing %s raises I/O error(%s):%s" % (tmp_pdf_path, errno, strerror), False
    finally:
        if f is not None:
            f.close()

    f = None
    try:
        p = subprocess.Popen([pdftotext_path, '-enc', 'Shift-JIS', tmp_pdf_path], stderr=subprocess.PIPE)
        if p.wait() != 0:
            return "%s" % (p.stderr.readlines()), False

        f = open(tmp_txt_path, "rb")
        original_text = unicode(f.read(), 'shift_jis').encode('utf-8')
        f.close()
        return original_text.encode('utf-8'), True

    except IOError, (errno, strerror):
        return "reading %s raises I/O error(%s):%s" % (tmp_txt_path, errno, strerror), False

    except OSError as e:
        return "OS Error(%s) pdftotext_path(%s)" % (e.errno, pdftotext_path), False

    finally:
        try:
            os.remove(tmp_pdf_path)
        except:
            pass
        try:
            os.remove(tmp_txt_path)
        except:
            pass
        if f is not None:
            f.close()
