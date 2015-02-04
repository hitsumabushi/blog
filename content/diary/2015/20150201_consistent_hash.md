Title: Consistent Algorithm
Date: 2015-02-01 00:33
Category: blog
Tags: Algorithm, Paper

Consistent Hash Algorithmという負荷分散などの目的で使えるアルゴリズムがある。
たまたまarxivでシンプルで高速, 省メモリな実装についての論文を見つけたので、読んだ。

## 読んだ内容
スライドにまとめた

<iframe src="//www.slideshare.net/slideshow/embed_code/44282881" width="476" height="400" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

## 疑問点

1. 論文では、キャッシュとしては使いづらい、という趣旨のことが書かれている。ノードのIDをかぶらせてもたせるだけではダメ?
2. ノードを削除するとき、ノード側でリバランスする必要があるが、その場合には別途方法を考える必要があるように思う。(IDの再計算はそんなに難しくはなさそうに思う)

