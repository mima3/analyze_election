# -*- coding: utf-8 -*-
from collections import defaultdict


class tf_idf_result:
    """
    tf-idfのスコアの結果を格納する
    """
    def __init__(self, category):
        self.category = category
        self.term_scores = defaultdict(int)

    def set_score(self, term, score):
        self.term_scores[term] = score
