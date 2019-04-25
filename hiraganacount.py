from hiraganautil import hiraganautil

words = hiraganautil.load_words("data/monohoshi.txt")
for hira_count in hiraganautil.get_hiragana_counts(words, sort_by_count=True):
    print(hira_count[0], hira_count[1])