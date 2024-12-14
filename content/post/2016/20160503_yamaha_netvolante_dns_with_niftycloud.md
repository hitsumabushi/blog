---
title: YAMAHAのネットボランチDNSを使って、ニフティクラウドとVPN接続する
date: 2016-05-03T06:24:00+09:00
slug: '0624'
aliases:
  - 0624.html
categories:
  - blog
tags:
  - vyos
  - YAMAHA
  - NIFTY
---


## やりたいこと

いろいろあって、自宅のグローバルIPv4アドレスが変更される機会があった。
ニフティクラウド上のルーターとVPN接続しているため、グローバルIPが変更されると、
いちいち変更されたタイミングでVPN設定を変更する必要があり、非常に面倒くさい。
そういうわけで、DDNSを使って設定することで、グローバルIPが変更された場合でも設定変更の必要がないようにしようと思う。


## ネットボランチDNSとは
[ネットボランチDNSは、YAMAHAが提供しているダイナミックDNSサービスのこと](http://www.rtpro.yamaha.co.jp/RT/FAQ/NetVolanteDNS/index.html)。
YAMAHAのルーターで利用可能。
別にネットボランチDNSじゃなくとも、世の中のDDNSサービスを使えば良いとは思うけど、
YAMAHAのルーターを使っている場合には、こちらの方が設定が簡単なので、今回はネットボランチDNSを利用する。

## 接続までの手順

以下は、YAMAHA RTX1200 (Rev.10.01.65) で実施している。
回線はフレッツ光ネクストで、IPv4側の接続はPPPoEになっている。
(今回は関係ないけど、IPv6側はIPoE。)

### ネットボランチDNSの登録

1. 登録状況の確認
今回はまだ何も登録されていないことを確認している。
```
# netvolante-dns get hostname list all

(Netvolante DNS server 1)
```
2. PPPoEで利用しているIPの登録
ホスト名を`example-yamaha`とすると以下のようにして登録を行う。
```
# pp select 1
pp1# netvolante-dns hostname host pp example-yamaha
pp1# netvolante-dns go pp 1

(Netvolante DNS server 1)
[example-rtx.aa0.netvolante.jp] を登録しました
新しい設定を保存しますか? (Y/N)Yセーブ中... usb1:/config.txt 終了
```
3. 登録の確認
登録状況の確認としては、ネットボランチ用のコマンドで確認することに加え、名前解決しておく。
```
pp1# netvolante-dns get hostname list all

(Netvolante DNS server 1)
PP01    example-rtx.aa0.netvolante.jp
# pp1# netvolante-dns go pp 1

(Netvolante DNS server 1)
```
```
pp1# show status netvolante-dns pp

(Netvolante DNS server 1)
ネットボランチDNSサービス:     AUTO
インタフェース:                PP[01]
ホストアドレス:                example-rtx.aa0.netvolante.jp
IPアドレス:                    <グローバルIPアドレス>
最終更新日時:                  2016/05/03 07:23:13
タイムアウト:                  90 秒

(Netvolante DNS server 2)
ネットボランチDNSサービス:     AUTO
インタフェース:                PP[01]
ホストアドレス:
IPアドレス:
最終更新日時:
タイムアウト:                  90 秒
```
```
pp1# nslookup example-rtx.aa0.netvolante.jp
<グローバルIPアドレス>
```

### ニフティクラウドでVPNゲートウェイを作成する

細かな作成手順などは、[YAMAHAさんのサイト](http://jp.yamaha.com/products/network/solution/dns_cloud/nifty_cloud/) にキャプチャつきで記載されているのえ、要点だけかいつまんで記載する。

カスタマーゲートウェイについては、以下のキャプチャの通りに作成した。
![](/images/2016/vpn/create_vpn_connection.png)

また、VPNコネクションについては、以下のキャプチャを参考にしてほしい。
![](/images/2016/vpn/customer_gateway.png)

すこしわかりにくいけど、VPNゲートウェイとカスタマーゲートウェイを結ぶ線をクリックすると、
![](/images/2016/vpn/network_line.png)

以下のような設定テンプレートをコピーできる
![](/images/2016/vpn/template.png)

このテンプレートを元に、YAMAHA RTX1200を設定すれば良い。
基本的には、テンプレートの内容をそのまま書くか、PPPoE用に書けば、だいたい大丈夫。
テンプレートに含まれていないこととして、フィルタを空けるというのがある。以下のような感じでやれば良い。
```
ip pp secure filter in ...(既存のフィルタ) 200080 200081 200082
ip filter 200080 pass * 192.168.100.1 udp * 500
ip filter 200081 pass * 192.168.100.1 esp * *
ip filter 200082 pass * 192.168.100.1 udp * 4500
```

## 疎通確認

YAMAHA RTX側で以下を実行すると良い
```
# show ipsec sa
Total: isakmp:2 send:1 recv:1

sa   sgw isakmp connection   dir  life[s] remote-id
-----------------------------------------------------------------------------
1     1    -    isakmp       -    27132   <VPNゲートウェイのIP>
2     1    -    isakmp       -    27144   <VPNゲートウェイのIP>
3     1    2    tun[001]esp  send 1944    <VPNゲートウェイのIP>
4     1    2    tun[001]esp  recv 1944    <VPNゲートウェイのIP>
```

さらに、クラウド側のローカルIPに向かって、pingを打って疎通確認をしておけば完璧。


## まとめ

ネットボランチDNSを使って、ニフティクラウドとIPSecで接続できるようにした。
IPを変更したり...というテストはそれほどちゃんとやっていないが、まあ通常のVPNの接続断と大差ないので、大丈夫だろうと楽観視している。
とりあえず、これで自宅環境で検証できることが増えるぞ。

