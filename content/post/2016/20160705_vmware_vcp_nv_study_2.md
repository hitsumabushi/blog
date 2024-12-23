---
title: VCP6-NV 試験勉強メモ 2日目
date: 2016-07-07T07:42:46+09:00
slug: '0742'
aliases:
  - 0742.html
categories:
  - blog
tags:
  - VMware
  - NSX
  - VCP
---


## VCP6-NV 受験シリーズ

+ [VMware VCP-NV (VCP6-NV) の試験を今週受けるので、試験について調べる]({filename}/diary/2016/20160705_vmware_vcp_nv.md)
+ [VCP6-NV 試験勉強メモ]({filename}/diary/2016/20160705_vmware_vcp_nv_study.md)
+ [VCP6-NV 試験勉強メモ 2日目]({filename}/diary/2016/20160705_vmware_vcp_nv_study_2.md)
+ [VCP6-NV 取得した]({filename}/diary/2016/20160705_vmware_vcp_nv_study_result.md)

## 資料
- [ネットワーク仮想化をネットワークの基本から理解する　〜 第1回：理解するために必要なことを整理する](http://blogs.vmware.com/jp-cim/2015/03/nwv01.html)
- [NSX 6.2 新機能のご紹介 Part 1 〜 Cross vCenter NSX 〜](https://blogs.vmware.com/networkvirtualization/2015/12/2366.html?lang=ja#.V3ve2WiLSUk)

## NSX におけるVXLAN

### 関係する要素
- 論理スイッチ
- 分散論理ルータ
- 論理ルータコントロール VM
- Edge

### 分散論理ルータ
カーネルモジュール内で動作するルーター。
各ESXiに分散して存在していて、ヘアピントラフィックを防ぐことができる。

分散論理ルータのインターフェースは、LIF(論理インターフェース)と呼ばれる。

- LIF
    - IPアドレスが割り当てられる
    - ARPテーブルはLIFごとに持つ
- vMAC
    - LIFが分散スイッチにささっている時のMAC
    - 物理スイッチに保存されることはない
    - VXLAN LIF の時のMACアドレス
        - VLAN LIFと違い、代表インスタンスなどは不要
        - 1つの論理スイッチに接続できるVXLAN LIFは1つ
        - トランスポートゾーン全体のDVSに広げることができる
- pMAC
    - LIFがポートグループにささっている時のMAC
    - 物理スイッチに保存される
    - VLAN LIF の時のMACアドレス
        - VLAN LIF は1台のDVSにのみ所属できる
        - VLAN LIF は代表インスタンスを1つ持ち、ARP要求はその代表インスタンスが処理する
            - 疑問: ARP要求は代表インスタンスが答えるが、実際には全てのホストで同じpMACを持っていて、その後のトラフィックは各ホストで処理するということで良いのか?
        - 代表インスタンスの選定は、NSX Controllerが行う

### 制御プレーンについて

分散論理ルータの制御プレーンは、以下の2つある。

- インスタンスごとに作られる、論理ルータコントロール仮想マシン
    - Active/Standby 構成にもできる
    - ダイナミックルーティング(OSPF, BGP)を処理する
        - つまり、隣接ノードから見ると、VLAN LIFとは異なるIPとセッションをはることになる
    - 処理したルーティング情報をNSX Controllerへ送る
- NSX Controller
    - ルーティング情報を分散ルータへ(つまり対象のすべてのESXiへ)プッシュする

## L2 ブリッジ

VXLAN と VLAN の L2ブリッジのみがサポートされる。
アップリンクをDVSに割り当てておけば、物理機器とVXLANをつなぐような用途で利用できる。

L2 ブリッジには分散ルータが必要で、論理ルータコントロール仮想マシンが載っているホストが、ブリッジインスタンスとして、実際のブリッジを行う。つまり、1ホストのラインレートが上限になる。
スループットを向上させるには、1つのブリッジに対しては1つの分散ルータを作成するようにすることが良い。

分散ルーティングと論理スイッチ上のブリッジは同時に有効にできない。

