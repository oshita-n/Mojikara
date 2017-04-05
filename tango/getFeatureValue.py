import sys
import os
import codecs
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer

count = CountVectorizer()
keywords = []
with codecs.open(os.path.join('./', sys.argv[1]), 'r', 'utf-8') as f:
    # keywords.append(f.read().split("。"))
    # content = np.array([f.read().split("。")])
    docs = np.array([f.read()])
    bag = count.fit_transform(docs)

    # tfidfの設定
    tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)
    # 小数点第4位まで表示する．
    np.set_printoptions(precision=4)
    cnt_voc = count.vocabulary_
    tfidf_array = np.array(tfidf.fit_transform(bag).toarray())

    # ベクトルと単語を対応づけるために必要な処理．
    vec = DictVectorizer()
    vec.fit_transform(cnt_voc).toarray()
    feature = vec.get_feature_names()

    # tfidfの閾値の設定
    threshold = 0.3

    # ヒットした要素の数字を代入する．なぜか二つの配列で渡される．
    hairetsu = np.where(tfidf_array >= threshold)
    # np.uniqueで重複する値を削除する．
    # なぜかnp.whereだと二つの配列が返ってくるので，連結して一つにする．
    hit_word = np.unique(np.append(hairetsu[0], hairetsu[1]))
    
    word = []
    # tfidfで計算された単語を出力する．
    for num in range(0, len(hit_word)):
        word.append(feature[hit_word[num]])

    # 出力結果がなかった場合，閾値を下げる
    if len(word) == 0:
        threshold = 0.2
        hairetsu = np.where(tfidf_array >= threshold)
        hit_word = np.unique(np.append(hairetsu[0], hairetsu[1]))
        word = []
        # tfidfで計算された単語を出力する．
        for num in range(0, len(hit_word)):
            word.append(feature[hit_word[num]])
    print(' '.join(word))
