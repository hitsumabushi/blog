---
title: Dockerのプロキシ設定
date: 2015-01-29T07:54:00+09:00
slug: '0754'
aliases:
  - 0754.html
categories:
  - blog
tags:
  - Docker
  - Debian
---

自宅ではプロキシを立てていないので問題なかったが、会社でDockerをいじろうとするとプロキシに阻まれてうまくいかず困っていた。
bashの環境変数を設定するのはうまくいかなくて、しばらく手元ではdockerをやらず、作業用マシンをクラウドに立ててどうにかごまかしていたのだけど、
あらためて考えると解決できた。

結論は、dockerのデーモンが起動するときに、プロキシの設定をしておく必要がある、というだけでした。
/etc/default/docker に以下を記載します。

```shell
    export http_proxy="プロキシのIP"
```



