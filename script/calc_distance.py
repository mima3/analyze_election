#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
import nltk
from tf_idf_result import tf_idf_result

def calc_distance(tf_idf_ret):
  """
  tf_idf のスコアを元に距離を取得します。
  ret[str] = float
  """
  result = defaultdict(dict)
  for fromCategory,fromTokens in tf_idf_ret.items():
    for toCategory,toTokens in tf_idf_ret.items():
      if fromCategory == toCategory:
        continue
      
      for f in fromTokens.term_scores:
        if f not in toTokens.term_scores:
          toTokens.set_score( f, 0 )

      for t in toTokens.term_scores:
        if t not in fromTokens.term_scores:
          fromTokens.set_score( t, 0 )

      v1 = [ score for (term, score) in sorted(fromTokens.term_scores.items())]
      v2 = [ score for (term, score) in sorted(toTokens.term_scores.items())]
      result[fromCategory][toCategory] = nltk.cluster.util.cosine_distance(v1,v2)
  return result
