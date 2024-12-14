---
title: ESXiのインストールをPXE bootせずに自動化したい
date: 2015-09-17T09:10:00+09:00
slug: '0910'
categories:
  - blog
tags:
  - VMware
  - ESXi
  - automation
draft: true
---

## 動機
PXEブートによるインストールでは、最初にサーバーとDHCPが通信する場合、サーバー側はVLANを利用できない。
DHCPサーバー側がVLANセグメントにいると、サーバーの上位スイッチの設定を変更し、untagしてもらう必要がある。

そのため、すでにサービス投入されているようなサーバーたちで、untagする用のネットワークがない場合、
ネットワーク構成を変更しづらいため、PXEブートによるインストールが難しい。
(と隣のチームの人が困っていた。)

世の中の企業が使っているような物理サーバーは、リモートからISOがマウントできたりするようなので、そのあたりの機能で自動インストールしてみる。

## 方法の概要
まず、半自動で良いなら、kickstartファイルを指定することで、大部分を自動化できる。
問題なのは、ISOをマウントする部分と、ISOからブートしたあとkickstartファイルを指定してインストールを進める部分になる。

まず、ESXiのISOをカスタマイズして、kickstartファイルを決め打ちで指定するようにし、その後ISOをマウントする部分を検討しよう。

### ISOのカスタマイズ

まずISOの中身を取り出す。

```sh
$ sudo mount -o iso9660 -o loop <ISO filename> /mnt
$ mkdir /tmp/workdir
$ cp -r /mnt* /tmp/workdir
$ chmod -R +w /tmp/workdir
$ sudo umount /mnt
```

次に、boot.cfg を編集する。

```
bootcfgの中身
```

ISOに固める。

```sh
$ genisoimage -relaxed-filenames -R -T -J -o custom.iso -b isolinux.bin -c boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table /tmp/workdir
```

```sh
$ genisoimage -relaxed-filenames -R -T -J -o ks.iso /tmp/20150917_ks
```

