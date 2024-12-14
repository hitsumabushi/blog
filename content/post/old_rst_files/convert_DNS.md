---
title: DNS サーバー
date: 2014-01-01T02:41:20+09:00
slug: 0241
tags:
  - dns
categories:
  - blog
---


ニフティクラウド上でサーバーを立てた。
いろいろと設定していこうかと思っているが、まずはDNSから始める。

## 作業内容

1\. /etc/bind/named.conf.options 以下のように書き換える:

    // v6の設定： v6は応答しない
    // listen-on-v6 { any; };
    listen-on-v6 { none; };

    // transfer を許すIPを制限
    allow-transfer "192.168.100.1";

2\. /etc/bind/named.conf.local ゾーンの設定:

    zone "example.com" {
       type master;
       file "example.db";
    };
    zone "100.168.192.in-addr.arpa" {
       type master;
       file "192.rev"
    };
