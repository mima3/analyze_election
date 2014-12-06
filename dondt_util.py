# coding=utf-8
import os
import re
from collections import defaultdict
import math
import json
import copy
import operator

class political_party_info:
    """
    政党の情報を格納するクラス
    name : 政党名
    votes:得票数
    max    :立候補者数（いくら得票してもこれをこえた議席は取得できない）
    seats:取得議席数
    """
    def __init__(self, name, votes, max):
        self.name = name
        self.votes = votes
        self.max = max
        self.seats = 0

def select_political_party(votes):
    """
    政党名をキー、値をpolitical_party_infoとしたディクショナリ中でもっとも得票している党名を取得する
    """
    max = -1
    ret = None
    for k, v in votes.items():
        # 同数の場合、本来くじで決めるが今回は登録順とする
        if max < v.votes:
            ret = k
            max = v.votes
    return ret

def dondt(votes_data, max):
    """
    ドント方式による
    votes_data: 政党名をキー、値をpolitical_party_infoとしたディクショナリ
    max:総議席数
    votes_data[x].seatsに議席数が格納されます。
    """
    tmp_votes = copy.deepcopy(votes_data)
    for i in range(1, max+1):
        s = select_political_party(tmp_votes)
        if s is None:
            return None
        votes_data[s].seats += 1
        tmp_votes[s].votes = math.floor(votes_data[s].votes / (votes_data[s].seats + 1))
        if tmp_votes[s].max == votes_data[s].seats:
            #立候補した数超えたので以降この政党への投票は無効
            tmp_votes[s].votes = 0
    return votes_data
