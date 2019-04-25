from hiraganautil import hiraganautil

words = hiraganautil.load_words("data/xmas.txt")
sorted_words = sorted(words)
for word in sorted_words:
    print(word)