---
title: Windowsのsysprepが正常に完了しないときに調べること
date: 2016-09-09T14:29:00+09:00
slug: 1429
categories:
  - blog
tags:
  - sysprep
  - windows
draft: true
---


## 経緯

windows 7 でsysprepが正常に完了しなかった。
具体的には、unattended.xmlがあるのに、 キーボードやライセンスの設定が表示されていた。
何が起こっているのか、ログを見たい。

## sysprepのログの場所

* generalize : `C:\Windows\System32\sysprep\Panther`
* specialize : `C:\Windows\Panther`
* Unattended : `C:\Windows\Panther\UnattendGC`

## ログファイル

* `setupact.log`
