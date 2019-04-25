import sys
from hiraganautil import hiraganautil


def judge_is_available(argv):
    if len(argv) != 2:
        return False

    if len(argv[1]) != 1:
        return False

    if argv[1] not in hiraganautil.aiueo:
        return False

    return True


if __name__ == "__main__":
    if judge_is_available(sys.argv):
        sub_word = sys.argv[1]
        words = hiraganautil.load_words("data/monohoshi.txt")
        filtered_words = hiraganautil.search_words(words, sub_word)

        for word in filtered_words:
            print(word)

        for hira_count in hiraganautil.get_hiragana_counts(filtered_words, sort_by_count=True):
            print(hira_count[0], hira_count[1])
    else:
        print("argv is not available")


