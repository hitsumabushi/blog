Title: Windowsのsysprepが正常に完了しないときに調べること
Date: 2016-09-09 14:29
Category: blog
Tags: sysprep, windows
Status: draft

[TOC]

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
