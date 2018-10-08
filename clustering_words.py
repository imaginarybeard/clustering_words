import unicodedata
import numpy as np
from sklearn.cluster import KMeans

num_of_char_limit = 6
n_clusters = 2
aiueo = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
komoji = "ぁぃぅぇぉっゃゅょゎ"
oomoji = "あいうえおつやゆよわ"
words_list = []


def convert_to_plane(char):
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


def show_chars_num(words):
    """
    ことばに含まれる文字をカウントするよ。
    """
    input_str = "".join(words)
    count_dict = {}
    for char in input_str:
        char = convert_to_plane(char)
        if char in count_dict:
            count_dict[char] += 1
        else:
            count_dict[char] = 1

    count_tuple = ((k, count_dict[k]) for k in count_dict)
    sorted_tuple = sorted(count_tuple, key=lambda x: x[0], reverse=False)

    for kv in sorted_tuple:
        print(kv[0], kv[1])


def word2vector(word):
    """
    ことばを43次元のベクトル（あ〜ん、存在すれば1、しなければ0）に変換するよ。
    """
    vector = np.zeros((len(aiueo), ), dtype="int")
    for char in word:
        char = convert_to_plane(char)
        i = aiueo.index(char)
        if(vector[i] == 0):
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


def recursive_clustering(words, word_vectors, k_means_classifier):
    """
    再帰的にことばのクラスタリングを行うよ。使用文字種がnum_of_char_limit以下になるまで分割するよ。
    """
    def check_num_of_char_limit(word_vectors):
        all_or = np.zeros(len(aiueo), "int")
        for word_vecor in word_vectors:
            all_or = np.logical_or(all_or, word_vecor)
        return int(np.linalg.norm(all_or.astype(int), ord=1)) <= num_of_char_limit

    if check_num_of_char_limit(word_vectors):
        words_list.append(words)
    else:
        predict = k_means_classifier.fit_predict(word_vectors)
        words_1 = []
        words_2 = []
        word_vectors_1 = np.empty((0, len(aiueo)), int)
        word_vectors_2 = np.empty((0, len(aiueo)), int)

        for i, word_vector in enumerate(word_vectors):
            if(predict[i] == 0):
                words_1.append(words[i])
                word_vectors_1 = np.append(word_vectors_1, word_vector.reshape(1, len(aiueo)), axis=0)
            elif(predict[i] == 1):
                words_2.append(words[i])
                word_vectors_2 = np.append(word_vectors_2, word_vector.reshape(1, len(aiueo)), axis=0)

        recursive_clustering(words_1, word_vectors_1, k_means_classifier)
        recursive_clustering(words_2, word_vectors_2, k_means_classifier)


if __name__ == "__main__":
    """
    メイン処理だよ。CUIでかつ、ことばファイルの読み込みの切り替えはソースのコメントアウトで対応してるよ。
    結果は標準出力にドバドバ出てくるよ。
    率直にいって手抜きだよ。
    """
    k_means_classifier = KMeans(n_clusters=n_clusters)

    # words = load_words("data/words_lt4.txt")
    # words = load_words("data/words_eq4.txt")
    words = load_words("data/words_eq5.txt")
    # words = load_words("data/words_eq6.txt")

    word_vectors = [word2vector(word) for word in words]
    recursive_clustering(words, word_vectors, k_means_classifier)
    words_list_sorted = sorted(words_list, key=lambda words: len(words), reverse=True)
    for words in words_list_sorted:
        print(words)
        show_chars_num(words)
        print()