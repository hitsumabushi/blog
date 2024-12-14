---
title: VMware NSX
date: 2015-03-16T09:58:00+09:00
slug: '0958'
categories:
  - blog
tags:
  - VMware
  - NSX
draft: true
---


## 資料
1. VMware NSX Network Virtualization Design Guide

## VCP-NVの概要
1. 言語: 英語 or 日本語 (日本語はしょぼそう)
2. 時間: 120分
3. 問題数: 120問
4. 問題形式: 選択式

## NSX Network Virtualization Design Guide
### Overview
Network Virtualizationの気持ちは、Server virtualizationと並行して理解すると良い。
- Server virtualizationによって、CPU, Mem, Storageのことが、物理層と仮想層で分離された。VMからはハイパーバイザで抽象化されている
- Network virtualizationによって、物理ネットワークと仮想ネットワークを分離したい。VMからは仮想ネットワークプラットフォームで抽象化したい
  + VMから見えるのは、IP transport層だけ
  + CPU poolに対応するもの = transport capacityのpool
  + スナップショット、削除、リストアをsoftware-definedでやる

### Introduction to Network Virtualization

1. Network Stacks

        | Layer | Components |
        |----------|---------|
        | Cloud Consumption | any apps. |
        | Management Plane | NSX Manager |
        | Control Plane | NSX Controller |
        | Data Plane | destributed services, hypervisor kernel modules(Logical SW, Destributed LR, FW), NSX Edge, ESXi |
        | Physical Network | physical components |

2. Planes
  - Control Plane
    + 3台以上の奇数台をデプロイする
    + 以下の制御を行う
      - multicast freeなVXLAN
      - DLR, DFWなどのプログラマブルな要素
  - Data Plane
    + NSX vSwitchから成る。
      - NSX vSwitchは、vSphere vDSとサービスを有効にするためのコンポーネントを合わせたもの
      - 追加のコンポーネントは、HypervisorにVIBとしてインストールされる
      - DLR, DFW, VXLAN bridging用のVIBがある
    + VXLANをオーバーレイネットワークのために利用
      - port mirroring, netflow/IPFIX, QoS, LACP, backup&restore, Health Check, ...
    + VLAN-VXLAN間のgatewayもData Planeに含まれる
      - これは、L2でも、L3でもありうる。(L2: NSX bridging, L3: NSX routing)
  - Management Plane and Consumption Platforms
    + REST APIや、UIなどを提供
    + Integrationに利用できるものとして、vCloud Automation Center(vCAC), vCloud Director(vCD)などがある

3. NSX Functional Services
  - Switching
  - Routing
    + overlay network上のトラフィックが、物理ルータに出ないようなルーティングをする
  - FW
    + vNICレベルでのFW
  - LB
    + L4-L7 load balancing
    + SSL termination
  - VPN
    + SSL VPN to enable L2, L3 VPN
  - Connectivity to Physical
    + L2, L3 Gateway functions

### NSX-v Functional Components
NSXは、Hypervisor Access Layerと、Gateway Access Layerという、2つのネットワークアクセスのレイヤを作っている。
Hypervisor Access LayerはVMが使うためのもので、Gateway Access Layerは、Edge Gatewayが使うためのもの。
つまり、物理層から見た時、オーバーレイのことを知らないとすれば、ハイパーバイザと通信しているか、ゲートウェイと通信しているか、の2つのトラフィックしかない。

1. NSX Manager
  Management Plane。vCenterと1:1になる。



