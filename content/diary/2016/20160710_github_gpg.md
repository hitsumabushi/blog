Title: GnuPG 2.xでgit commitに署名をしようとするとエラーが出るメモ
Date: 2016-07-10 01:46
Category: blog
Tags: git, gpg
Status: draft

[TOC]

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
