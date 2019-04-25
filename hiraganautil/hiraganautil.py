import sys
import unicodedata
import numpy as np

aiueo = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
komoji = "ぁぃぅぇぉっゃゅょゎ"
oomoji = "あいうえおつやゆよわ"


def hiragana2plane(char):
    """
    濁音、半濁音、小文字をプレーンなひらがなに直すよ。
    """
    try:
        i = komoji.index(char)
        char = oomoji[i]
    except ValueError:
        pass
    char = unicodedata.normalize("NFKD", char)[0]
    return char


def get_hiragana_counts(words, sort_by_count=False):
    """
    ことば群に含まれる文字を数えて((ひらがな, 個数), ...)で返すよ
    """
    input_str = "".join(words)
    count_dict = {}
    for char in input_str:
        char = hiragana2plane(char)
        if char in count_dict:
            count_dict[char] += 1
        else:
            count_dict[char] = 1

    count_tuple = ((k, count_dict[k]) for k in count_dict)
    if sort_by_count:
        sorted_tuple = sorted(count_tuple, key=lambda x: x[1], reverse=True)
    else:
        sorted_tuple = sorted(count_tuple, key=lambda x: x[0], reverse=False)
    return sorted_tuple


def word2vector(word, keep_away_chars="にぬねむるれ"):
    """
    ことばを43次元のベクトル（あ〜ん、存在すれば1、しなければ0）に変換するよ。
    """
    vector = np.zeros((len(aiueo), ), dtype="int")
    for char in word:
        char = hiragana2plane(char)
        try:
            i = aiueo.index(char)
        except ValueError as e:
            print(e, word)
            sys.exit(0)

        if vector[i] == 0:
            if char in keep_away_chars:  # 一部希少文字のみ分離
                vector[i] = 3
            else:
                vector[i] = 1

    return vector


def load_words(path):
    """
    改行で区切ったことばファイルを読み込むよ。
    """
    words = []
    try:
        with open(path, "r", encoding='utf-8') as f:
            words = f.readlines()
    except IOError:
        pass
    return [word.replace("\n", "") for word in words]


def search_words(words, sub_word):
    return [word for word in words if sub_word in word]
