from hiraganautil import hiraganautil
import numpy as np
from sklearn.cluster import KMeans

num_of_char_limit = 6
n_clusters = 2

keep_away_chars = "にぬむれ"
words_list = []


def recursive_clustering(words, word_vectors, k_means_classifier):
    """
    再帰的にことばのクラスタリングを行うよ。使用文字種がnum_of_char_limit以下になるまで分割するよ。
    """
    def check_num_of_char_limit(word_vectors):
        all_or = np.zeros(len(hiraganautil.aiueo), "int")
        for word_vecor in word_vectors:
            all_or = np.logical_or(all_or, word_vecor)
        return int(np.linalg.norm(all_or.astype(int), ord=1)) <= num_of_char_limit

    if check_num_of_char_limit(word_vectors):
        words_list.append(words)
    else:
        predict = k_means_classifier.fit_predict(word_vectors)
        words_1 = []
        words_2 = []
        word_vectors_1 = np.empty((0, len(hiraganautil.aiueo)), int)
        word_vectors_2 = np.empty((0, len(hiraganautil.aiueo)), int)

        for i, word_vector in enumerate(word_vectors):
            if predict[i] == 0:
                words_1.append(words[i])
                word_vectors_1 = np.append(word_vectors_1, word_vector.reshape(1, len(hiraganautil.aiueo)), axis=0)
            elif predict[i] == 1:
                words_2.append(words[i])
                word_vectors_2 = np.append(word_vectors_2, word_vector.reshape(1, len(hiraganautil.aiueo)), axis=0)

        recursive_clustering(words_1, word_vectors_1, k_means_classifier)
        recursive_clustering(words_2, word_vectors_2, k_means_classifier)


if __name__ == "__main__":
    """
    メイン処理だよ。CUIでかつ、ことばファイルの読み込みの切り替えはソースのコメントアウトで対応してるよ。
    結果は標準出力にドバドバ出てくるよ。
    率直にいって手抜きだよ。
    """
    k_means_classifier = KMeans(n_clusters=n_clusters, n_init=1000)

    # words = hiraganautil.load_words("data/words_lt4.txt")
    # words = hiraganautil.load_words("data/words_eq4.txt")
    # words = hiraganautil.load_words("data/words_eq5.txt")
    # words = hiraganautil.load_words("data/words_eq6.txt")
    # words = hiraganautil.load_words("data/okashi.txt")
    # words = hiraganautil.load_words("data/monohoshi.txt")
    words = hiraganautil.load_words("data/eva.txt")
    # words = hiraganautil.load_words("data/mono_ya.txt")

    word_vectors = [hiraganautil.word2vector(word, keep_away_chars=keep_away_chars) for word in words]
    recursive_clustering(words, word_vectors, k_means_classifier)
    words_list_sorted = sorted(words_list, key=lambda words: len(words), reverse=True)
    for words in words_list_sorted:
        print(words)
        for hira_count in hiraganautil.get_hiragana_counts(words):
            print(hira_count[0], hira_count[1])
        print()