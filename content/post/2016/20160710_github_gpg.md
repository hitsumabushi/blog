---
title: GnuPG 2.xでgit commitに署名をしようとするとエラーが出るメモ
date: 2016-07-10T01:46:00+09:00
slug: '0146'
categories:
  - blog
tags:
  - git
  - gpg
draft: true
---


## 参考

* http://www.zsh.org/mla/users/2015/msg01173.html

## エラー内容

```
$ git commit -m "commit"
gpg: signing failed: Inappropriate ioctl for device
gpg: signing failed: Inappropriate ioctl for device
error: gpg failed to sign the data
fatal: failed to write commit object
```

## 対処

`GPG_TTY=$(tty)` として、ttyを指定すれば良いらしい。
どうも、署名をするときのパスフレーズを入力する画面を表示しようとしてエラーが出ているように見える。

## 余談

.gitconfig をgitで管理しているので、マシンに依存する設定を分割している。
今のところは鍵もわけることにしている。

.gitconifg
```
[include]
path=.gitconfig.local
...
```

.gitconfig.local
```
[user]
signingkey = (鍵ID)
[commit]
gpgsign = true
[gpg]
program = gpg2
```
