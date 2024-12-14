---
title: vSphere 6.0 でのHA機能のエンハンスの要点
date: 2015-12-08T05:51:00+09:00
slug: 0551
categories:
  - blog
tags:
  - VMware
  - vSphere
---


## まとめ
 1. vSphere 6からは、ストレージパスが死んだ場合でもHAを設定できるようになった。
 2. vCenterは watchdogs によりプロセス落下時には再起動される
 3. vCenterの可用性をさらに高めるにはWindows版を利用し、MSCSクラスタを設定する必要がある

## 資料
1. [VMware vSphere 6 のドキュメント
](http://www.vmware.com/jp/support/support-resources/pubs/vsphere-esxi-vcenter-server-6-pubs)
2. [http://www.vmware.com/files/pdf/vsphere/VMW-WP-vSPHR-Whats-New-6-0-PLTFRM.pdf](http://www.vmware.com/files/pdf/vsphere/VMW-WP-vSPHR-Whats-New-6-0-PLTFRM.pdf)
3. [vSphere 5.x および 6.x での永続的なデバイスの損失 (PDL) と全パス ダウン (APD) (2081089)](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2081089)

## vSphere 5.5 までの障害あるある(Part 1)
物理ホストのHBAが死んだり経路上の問題で、特定のホスト群のみストレージへのパスが切れた。
vSphere 5.5 までは、ストレージへのパスが死んだ場合、HAによる保護ができない障害パターンで、IOが止まっているが、管理者が別のホストに移してから再起動するまでアプリケーションは死んでいた。

### vSphere 6になると...
VMCP(Virtual Machine Component Protection) の機能として、ストレージへのパスが切れた時に検知し、挙動を制御できる。
VMware のドキュメントとしては、`APL` と `PDL` という2つの用語に分かれていて、設定上も異なる設定が可能。

- `APL`
    - All path down
    - 全パスが切れた場合
- `PDL`
    - Permanent device loss
    - LUNがぶっ壊れて認識できなくなった場合など
    - どういう状態かは[KB 208108](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2081089)に例がある

## vSphere 5.5 までの障害あるある(Part 2)
vCenterのプロセスが落ちる。
仕方ないので、再起動させるスクリプトを書く。

### vSphere 6になると...
`Watchdog`がvCenterに組み込まれている。
 `PID Watchdog` と `API Watchdog`があって、それぞれプロセス自身を監視するのか、API経由で監視するのかの違いがある。 `API Watchdog` はデフォルトで起動する。
`Watchdog` は、vCenterプロセスの再起動してくれる。2回プロセス再起動してもプロセスが上がらない場合には、リブートする。

## vSphere 6以降の設計ポイント
(今までもやっていたと思うけど、 )VMCPのおかげで、1クラスタの中でストレージの障害範囲を分けておけば、 HAしてくれるようになった。
そのため、クラスタ内でストレージ機器への接続で、同一のスイッチを使わないようにするなど、検討する必要がある。

ところで、今回はvSphere 6で設計上の大きなポイントになる(と思っている)PSCについて一切触れていない。
PSCの構成については、[List of recommended topologies for VMware vSphere 6.0.x (2108548)](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2108548) に詳しく記載されている。
とはいえ、日本語版はアップデートされていないようだし、気が向いたら書こうとは思う。

