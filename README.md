## ことばクラスタリングくん一号

### 概要

1. "pythonが読める、書ける方用の手抜きプログラムです"
1. コトダマンの「ことば」の効率的な回収を目的としたクラスタリングツールです。
1. 同じひらがなを使用したことば群に分割できるから、デッキ構成の手間が減ります。
1. ただ、有用なのは2-4文字まで。5文字以降は1単語1デッキ構成の方がおそらく効率が良いです。
1. この手抜きプログラムが原因で発生したいかなる損害も保証し兼ねます。

### 使い方（てきとう）

1. （data内に「ことばを改行で区切ったテキストファイル」を作成します。）
1. ソースを弄って読み込むファイルを選択します。
1. python clustering_words.py で標準出力にドバドバ出ます。