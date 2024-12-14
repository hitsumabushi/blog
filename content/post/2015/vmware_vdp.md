---
title: VMware VDP, VDPA
date: 2015-01-07T19:24:00+09:00
slug: '1924'
aliases:
  - 1924.html
categories:
  - blog
tags:
  - VMware
  - VCP
  - VDP
---


## VMware Data Protection
### 資料
- [vSphere 5.5 の新機能紹介 - VMware Blogs](http://blogs.vmware.com/jp-cim/2013/12/vsphere-55-vdpa.html)
- [VMware vSphere Data Protection のドキュメント](http://www.vmware.com/jp/support/support-resources/pubs/vdr_pubs)

### 概要
VMware Data Recoveryの後継みたいなものっぽい。

VDRから発展した点としては、以下があある。

1. FLR(File Level Restore) をサポート
2. サポート台数の増加

### ライセンス体系

- VMware Data Protection
- VMware Data Protection Advanced
の2つあって、いくつか違いがあります。特に、容量について、VMware Data Protectionは2TBまで。

#### VDPとVDPAの違い
0. dedupストレージの上限拡大(2TBから8TBになる)
1. バックアップ データ レプリケーション
2. Microsoft SharePoint 対応エージェント
3. EMC Data Domain システムへのバックアップ (元々は、vmdkにしか保存できない)
4. 自動バックアップ検証機能 (一時的なVMにリストアして、vmware-toolsのハートビートを検証。NICは抜いてある)

以下の比較図は、[vSphere 5.5 の新機能紹介 - VMware Blogs](http://blogs.vmware.com/jp-cim/2013/12/vsphere-55-vdpa.html)からのもの。
![VDP と VDPAの違いの表](/images/2014/vpd_vdpa.png)


