---
title: Travis CIで git submodule update --init --recursive を止める
date: 2017-10-17T03:36:00+09:00
slug: 0336
categories:
  - blog
tags:
  - git
  - travis-ci
---


## 結論
- [https://docs.travis-ci.com/user/common-build-problems/#Git-Submodules-are-not-updated-correctly](https://docs.travis-ci.com/user/common-build-problems/#Git-Submodules-are-not-updated-correctly) に書かれている通り、 .travis.yml に以下の行を付け加えれば良い。
```
git:
  submodule: false
```
- 個別に `git submodule update --init hoge` していくとき、ビルドのトップディレクトリに戻りたくなることがある。この場合には、 `$TRAVIS_BUILD_DIR` を使えば良い。

## 経緯
久しぶりにこのブログを書いたらビルドに失敗していた。
原因としては、このブログで利用している [getpelican/pelican-plugins](https://github.com/getpelican/pelican-plugins) のsubmoduleの設定によって、
取得できないsubmoduleがあり、 `git submodule update --init --recursive` に失敗しているという感じだった。

## ハマった点
もともと、自分自身で .travis.yml の `install` で `git submodule update --init --recursive` していて、そこが悪いと思っていた。
そのため、必要なsubmoduleについて、個別に `git submodule update --init hoge` していって終わりだと思った。
実際にやってみると、 [https://travis-ci.org/hitsumabushi/blog/builds/288689875](https://travis-ci.org/hitsumabushi/blog/builds/288689875) のようになるが、install よりも早い段階でエラーになっていることに気づくのに時間がかかった。

