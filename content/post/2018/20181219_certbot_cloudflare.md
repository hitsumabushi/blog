---
title: cloudflare dns を利用したlet's encrypt の証明書更新
date: 2018-12-19T20:13:00+09:00
slug: '2013'
aliases:
  - 2013.html
categories:
  - blog
tags:
draft: true
---

## やること

プライベートなサーバーの名前解決に Cloudflare のDNSを利用しています。
この状況で、証明書が欲しくなったので、certbot を使ってLet's Encrypt の証明書を利用できるようにします。

## 証明書発行

```
$ sudo cat /opt/certbot-cloudflare/cf.ini
dns_cloudflare_email = <mail address>
dns_cloudflare_api_key = <api key>
$ docker run -it --rm -v /opt/certbot-cloudflare/cf.ini:/tmp/cf.ini:ro -v /etc/letsencrypt:/etc/letsencrypt --name certbot-dns-cloudflare certbot/dns-cloudflare renew --dns-cloudflare --dns-cloudflare-credentials /tmp/cf.ini -d _domain_
# いろいろ入力する
```

## crontab で証明書更新する
```
$ cat /etc/cron.d/certbot-dns-cloudflare 
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

* * */10 * *   root     docker run -it --rm -v /opt/certbot-cloudflare/cf.ini:/tmp/cf.ini:ro -v /etc/letsencrypt:/etc/letsencrypt --name certbot-dns-cloudflare certbot/dns-cloudflare certonly --dns-cloudflare --dns-cloudflare-credentials /tmp/cf.ini -d _domain_
```

## docker daemon をTLSにしてみる
```
$ cat /etc/systemd/system/docker.service.d/override.conf 
[Service]
Environment="DOCKER_NETWORK_OPTIONS=--dns 1.1.1.1"
ExecStart=
ExecStart=/usr/bin/dockerd -H unix:// -H tcp://0.0.0.0:2376 --tlsverify --tlscacert "/etc/letsencrypt/live/_domain_/chain.pem" --tlscert "/etc/letsencrypt/live/_domain_/cert.pem" --tlskey "/etc/letsencrypt/live/_domain_/privkey.pem"

$ sudo systemctl daemon-reload
$ sudo systemctl restart docker.service
```