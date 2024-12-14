---
title: もともとgitで管理されているアプリケーションをdebパッケージにしたいというメモ
date: 2016-07-11T04:28:00+09:00
slug: '0428'
aliases:
  - 0428.html
categories:
  - blog
tags:
  - debian
  - deb
  - package
  - apt
---


## はじめに

debパッケージを作る経験が少ないので、あまり良い方法ではないかもしれない。

## サンプル

https://github.com/hitsumabushi/hub

## 手順

```sh
# install
sudo apt install fakeroot

# tag, release をきれいにする
git tag -l > tag_list
for x in $(cat tag_list); do git push origin :$x ; done

# 色々リポジトリを整理した後、空っぽの masterを作る
git checkout --orphan master

# 自前で control, copyright ファイルを書く
# アップストリームのものを持ってくる
# 参考: https://github.com/bcandrea/consul-deb/tree/debian/debian
fakeroot dpkg-deb --build pkg tmp

# 生成された deb ファイルの中身を確認し、install してみる
ar x <deb file>
# ... check files
sudo dpkg -i <deb file>
# ... check installation
# dpkg -s <package>
# dpkg -L <package>

# 問題がなければ
git commit -a
git push origin master
```

