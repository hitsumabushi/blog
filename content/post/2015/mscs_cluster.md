---
title: vSphere 5.5環境でMSCSクラスタを組むときの制約
date: 2015-01-07T20:29:00+09:00
slug: '2029'
categories:
  - blog
tags:
  - VMware
  - VCP
  - Microsoft
  - MSCS
---


## 資料
MSCSのサポート状況

  - [VMware KB: Microsoft Cluster Service (MSCS) support on ESXi/ESX](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1004617)
  - [VMware KB: MSCS support enhancements in vSphere 5.5](http://kb.vmware.com/selfservice/search.do?cmd=displayKC&docType=kc&docTypeID=DT_KB_1_1&externalId=2052238)

MSCSとは

  - [http://www.atmarkit.co.jp/ait/articles/0812/03/news138\_5.html](http://www.atmarkit.co.jp/ait/articles/0812/03/news138_5.html)

## MSCS
Microsoft Cluster Serviceのこと。
MSFC(Microsoft Failover Cluster)と名称が変わっているけど、未だにMSCSと呼ばれる場合もある。

複数台について、フェイルオーバー型のクラスタを組める。
1台だけをマスターにして、他は待機系として構成する。

## VMware環境での利用
### クラスタリング一般の注意
クラスタリングのハートビートとして、

* ハートビート ネットワーク
* 共有ディスク(クォラムディスク)

が存在するものが多い。
この2つは構成上重要なので、以下ではここに注目する。

### サポートされている構成
3種類のクラスタリング構成がサポートされている。

1. 1つのホストでの MSCS 仮想マシンのクラスタリング （CIB）
2. 物理ホスト間での MSCS 仮想マシンのクラスタリング （CAB）
3. MSCS 仮想マシンを使用した物理マシンのクラスタリング （N+1）
    ※ この構成は、スタンバイ用のホスト1台を置いておき、他のホストのものとクラスタリングするもの。

### 制約
| コンポーネント | 条件                                 |
|---------------|---------------------------------------|
| 仮想SCSIアダプタ | Windows 2003 => LSI Logicパラレル, 2008 => LSI Logic SAS | 
| ディスクフォーマット | シックプロビジョニング、かつ、eagerzeroedthick |
| 共有ストレージ (CIB) | 仮想ディスクが推奨。仮想RDMも可 |
| 共有ストレージ (CAB) | 物理RDMが推奨。仮想RDMも可  |
| 共有ストレージ (N+1) | 物理RDMが利用可能 |
| ストレージアダプタ | ざっくりいうと、iSCSI, FCoEはサポートされている |

### その他の制限事項
* NFSディスク上のクラスタリングは不可
* NPIV不可
* FTとの併用不可

など。

