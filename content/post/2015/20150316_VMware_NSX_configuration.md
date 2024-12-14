---
title: VMware NSX Configuration
date: 2015-03-16T13:45:00+09:00
slug: '1345'
categories:
  - blog
tags:
  - VMware
  - NSX
draft: true
---


## 知っておくこと
1. コマンドのあと、"?"をつけると、ヘルプ

## コマンド
### Controller
1. Cluster status

      ```sh
      # controllerのクラスタ参加やサービスの状況がわかる。
      # クラスタIDは、最初のコントローラと同じ。
      show control-cluster status
      # ActiveなコントローラのIPを表示
      show control-cluster startup-nodes
      # 各ロールごとのステータスがわかる。マスター情報もある
      show control-cluster roles
      # connectionのlistening, openingの状況がわかる
      ## master nodeでは、 server, client, systemの数が上がる
      ## slave nodeでは、electionの数が上がる
      show control-cluster connections
      ```

### LDR
1. DIの確認
  ESXi上で、net-vdrコマンドを利用

    ```sh
    net-vdr --lif ...
    ```

### ESG
1. パケットのキャプチャ

    ```sh
    debug packet display interface vNic_0 port_80
    ```

## メモ
- LIFの用途
  1. 内部向け
    - 各ESXiで同じvMAC, 同じIPを利用
  2. アップリンク
    - pMAC(not vmnicのMACアドレス)として、物理ネットワークから認識される
    - 各ESXiごとに異なるpMACを利用する。IPは同じ。
    - DI: designated instance:(ARPの応答をするやつ。IPが同じ、異なるMACのLIFがあるので、必要)
- LIFの種類
  1. VLAN LIF
    vDS/vSSに接続。UpLinkではDIが選出。
  2. VXLAN LIF
    LSWに接続し、DIを選出しない
- LSWには、DLRのLIFは1つまで。もっとルータが欲しかったら、ESGWをつける。
  

- DLR固有のもの
  1. プロトコルアドレス
    ルーティングプロトコルのために、コントロールVMが利用
  2. 転送アドレス
    データプレーンのために、分散ルーターカーネルが利用
