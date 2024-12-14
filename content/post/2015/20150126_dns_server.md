---
title: DNS サーバーの比較資料集め
date: 2015-01-26T03:12:00+09:00
slug: 0312
categories:
  - blog
tags:
  - DNS
  - Debian
---

自宅開発環境を一新するついでに、真面目にサーバー構成を見直すことにした。
DNSサーバーは今までbind+dnsmasqでやっていたが、改めてパフォーマンスの観点から選定したい。
以下に、参考ページを列挙する。


## 参考になるページ
### 権威サーバ
- [DNSサーバパフォーマンス評価](http://jprs.co.jp/enum/enum_jprs/activity/pdf/N+I-20050610-C24.pdf)
- [NicTool](https://github.com/msimerson/NicTool/wiki/Install-Nameserver)
- [PowerDNS + NSD で DNS を構築する](http://blog.akagi.jp/archives/4072.html)
### キャッシュサーバ
- [DNSキャッシュサーバ 設計と運用のノウハウ](http://dnsops.jp/event/20140626/DNS-design-operation-higashi.pdf)
- [DNSキャッシュサーバ チューニングの勘所](http://www.slideshare.net/hdais/dns-32071366)
- [日本Unboundユーザー会](http://unbound.jp/unbound/)

## 内容
### 権威サーバ
BIND, PowerDNS, NSD, Knot, Yadifaなどの実装がある。
BINDしか知らない人に対する注意点として、上記のDNSサーバの多くは、権威サーバとしてしか動作しない、ということがある。

BINDではしばしば問題にされているのを見るが、権威サーバとキャッシュサーバは分けておくほうがセキュリティ上のリスクは減るので、いっそ異なるサーバを使うようにしたいと思う。

特に、NSD, Knot, Yadifaはパフォーマンスが優れている。
パフォーマンスについては、以下のページを見ると良い。

- [Benchmark - Knot DNS](https://www.knot-dns.cz/pages/benchmark.html#tab-response-rate)
- [Benchmark - Yadifa](http://www.yadifa.eu/benchmark)

### キャッシュサーバ
BIND, Unboundなどがあるよう。
[Unbound/NSD最新情報（OSC 2013 Tokyo/Spring）](http://www.slideshare.net/ttkzw/unboundnsdosc-2013-tokyospring-16708977)を見ると、Unbound(, NSD3, NSD4)の概要がわかる。




