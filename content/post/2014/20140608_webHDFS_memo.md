---
title: WebHDFSで詰まったこと
date: 2014-06-08T16:33:00+09:00
slug: '1633'
categories:
  - blog
tags:
  - Hadoop
  - WebHDFS
---


## 困っていたこと
HDFSでwebhdfsを使うとき、基本的にnamenodeにリクエストを投げればよいが、実データにアクセスするにはdatanodeにアクセスする。
ただ、使うときにはあんまり気にしなくて良くて、リクエストを投げればリダイレクト先を指定してくれる、らしい。
しかし、実際にやっているとうまくいかないケースがあった。

```shell
% LANG=C; curl -i "http://namenode:50070/webhdfs/v1/tmp/client.retry?op=open"
HTTP/1.1 307 TEMPORARY_REDIRECT
Cache-Control: no-cache
Expires: Mon, 02 Jun 2014 20:27:09 GMT
Date: Mon, 02 Jun 2014 20:27:09 GMT
Pragma: no-cache
Expires: Mon, 02 Jun 2014 20:27:09 GMT
Date: Mon, 02 Jun 2014 20:27:09 GMT
Pragma: no-cache
Content-Type: application/octet-stream
Location: http://localhost:50075/webhdfs/v1/tmp/client.retry?op=OPEN&namenoderpcaddress=namenode:8020&offset=0
Content-Length: 0
Server: Jetty(6.1.26)
```

## 解決
これは簡単で、ホスト名の設定がおかしい。

``` sh
   hostname
   # => hostname.example.com
```
となるだけではダメで、

``` sh
   hostname -f
   # => (ダメな例)localhost
   # => (正しい例)hostname.example.com
```
となるようにしないといけない。
CentOS初めて使ったけど、ドメイン名がどこで決まるかとか、難しいな。

