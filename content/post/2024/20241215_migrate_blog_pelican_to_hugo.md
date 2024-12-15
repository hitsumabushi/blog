---
title: 'このブログをPelicanからHugoに載せ替えた'
date: '2024-12-15T19:33:28+09:00'
author: hitsumabushi
categories: blog
tags:
    - hugo
    - pelican
keywords: ["hugo", "pelican"]
---

## なぜ変更したか?

[Pelicanは2014年から使っていたよう](https://www.hitsumabushi.org/blog/2014/12/15/2300/)で、そこまで文句があったわけではないが、やはり速度が気になっていた。それに加えて、どうしてもたまにバージョンアップして互換性が壊れたりして、たまに時間を取られていた。今回少し修正したいことがあったのだが、これを機に載せ替えるか、と載せ替えることにした。

載せ替え先の候補としては色々あったが、そこまで時間を使いたいわけではないので、利用者が多く、かつ、何かあったら自分がクイックに調べられる言語のものということで、Hugoを選択した。

## やったこと

[OctopressからHugoへ移行する方法](https://gam0022.net/blog/2016/09/25/migrated-from-octopress-to-hugo/#hugo%E8%A8%98%E4%BA%8B%E3%81%B8%E8%A8%98%E4%BA%8B%E3%81%AE%E7%A7%BB%E8%A1%8C%E3%81%99%E3%82%8B) のブログを主に参考にさせてもらった。
上記の記事は、Octpresssなので若干違っているが、stepとしてはPelicanでも近いことをやれば良い。

もともとのmarkdownから、`Title` を `title` に書き換えたりをsedでやりつつ、置き換えていけば大抵問題ない。

## パーマリンクについて

一方で、パーマリンクを同じにするところは非常に悩ましかった。

これまでの形式は、 `{base_url}/blog/{yyyy}/{mm}/{dd}/{HHMM}.html` という形式だった。 デフォルトのHugoのURLは `{base_url}/blog/about/` のようなpretty形式で、これを変更するには [uglyURLs を trueにすれば良い](https://gohugo.io/content-management/urls/#appearance)。sectionごとに有効かもできるため、古い記事だけ有効化しても良かった。

ただ、色々な種類のURLを1つのサイトに混ぜたくはないし、pretty-styleのURLのほうが、ugly-styleのURLよりも、URL文字列としてわかりやすい(し、わかりやすくなるように書かれることが多い)、という主張もわかる。
せっかく業務ではないので、これまでのURL形式を捨てて、
- 新しいコンテンツはpretty
- 古いコンテンツはugly-styleのアクセスも許す
ということにした。

これを達成するために、まずは、新しいpostは `/blog/:year/:month/:day/:slug/` という形式にすることにした。これは、configで以下のような設定になる。
```toml
[permalinks]
  post = "/blog/:year/:month/:day/:slug/"
````

ここで、slugを明示的に指定しない場合には適当なものが使われる。しかし、古いものは、 `HHMM.html` が入ってほしい。そこで、既存のコンテンツファイルに、そのdateを見て、slugを書く。(19:33の例)
```markdown
---
...
slug: '1933'
...
---
```

ここまででは、 `/blog/:year/:month/:day/:slug/` の形式にアクセスできるようになっただけで、 `/blog/{yyyy}/{mm}/{dd}/{HHMM}.html` という形式ではアクセスできない。
そのために [aliasesを使う](https://gohugo.io/content-management/urls/)。

```markdown
---
...
slug: '1933'
aliases:
  - 1933.html
...
---
```

こうすることで、`/blog/{yyyy}/{mm}/{dd}/{HHMM}.html` にアクセスすると、 `/blog/{yyyy}/{mm}/{dd}/{HHMM}/`にリダイレクトされるようになり、既存のURLでひとまずアクセスは可能になる。
uglyにした場合に、URLのリンクだけでも一貫したURLの形式にしたい、などあれば、もしかしたらaliasesでできるかもしれない。

## その他

検索機能のために、algoliaまわりの設定もしたのだが、もう少し変更したいところがあるので、まだ思い通りにはなっていないため割愛。
searchはそんなに容量がデカくないのもあってpelicanの事前生成ファイル+js方式でも困っていなかったが、使っているテーマ(https://github.com/zhaohuabing/hugo-theme-cleanwhite) 的にはalgoliaを使うのが楽そうだったので利用している。
