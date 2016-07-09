Title: VCP6-NV 試験勉強メモ
Date: 2016-07-05 21:21
Category: blog
Tags: VMware, NSX, VCP

[TOC]

## VCP6-NV 受験シリーズ

+ [VMware VCP-NV (VCP6-NV) の試験を今週受けるので、試験について調べる]({filename}/diary/2016/20160705_vmware_vcp_nv.md)
+ [VCP6-NV 試験勉強メモ]({filename}/diary/2016/20160705_vmware_vcp_nv_study.md)
+ [VCP6-NV 試験勉強メモ 2日目]({filename}/diary/2016/20160705_vmware_vcp_nv_study_2.md)
+ [VCP6-NV 取得した]({filename}/diary/2016/20160705_vmware_vcp_nv_study_result.md)

## 資料

### 最も公式っぽい資料
* [VMware Certified Professional 6 – Network Virtualization Exam](https://mylearn.vmware.com/mgrReg/plan.cfm?plan=64297&ui=www_cert) の "How to Prepare" に書いているもの。
* [Reference Design: VMware® NSX for vSphere (NSX) Network Virtualization Design Guide](https://www.vmware.com/files/pdf/products/nsx/vmw-nsx-network-virtualization-design-guide.pdf)
* [VCP6-NV (2V0-641) Practice Exam](http://mylearn.vmware.com/quiz.cfm?item=57466)

### ブログ : シリーズものは一通り目を通した方が良い
* [ネットワーク仮想化をネットワークの基本から理解する　〜 第1回：理解するために必要なことを整理する](http://blogs.vmware.com/jp-cim/2015/03/nwv01.html)
* [NSX 6.2 新機能のご紹介 Part 1 〜 Cross vCenter NSX 〜](https://blogs.vmware.com/networkvirtualization/2015/12/2366.html?lang=ja#.V3ve2WiLSUk)

## NSXの configuration maximums

[vSphere 製品のように](https://www.vmware.com/pdf/vsphere6/r60/vsphere-60-configuration-maximums.pdf) 公開されているわけではない。
でも、以下のサイトのように、情報を公開している人はいる。

* [NSX-V 6.1 Configuration Maximums](https://d-fens.ch/2015/02/16/nsx-v-6-1-configuration-maximums/)
* [VMware NSX-v Configuration Maximums](https://www.vmguru.com/2015/03/vmware-nsx-v-configuration-maximums/)

会社でNSX使っている人は、VMwareの人に言えば上限値資料もらえると思うけど、会社外で確認したいときに、便利。
運用・開発を考える場合でも、上限値系は何も見ずに言えることが望ましいと思う。
おおざっぱな各上限値のオーダーは頭に入れておきたいところ...なんだけど、NSX 6.1と6.2で数値が違うところがあるんだよなぁ。

## VCP6-NV (2V0-641) Practice Exam の問題抜粋

* 上限値系
    + Q. "What is the maximum number of VNIs that can be used in a vSphere environment?"
        * 10,000
        * これは、NSXの制限というよりは、 vCenterの制限かもしれない※要確認
        * VNIを1つ使うごとにポートグループを作ってしまう。現状のvSphere 6.0では、 10,000 portgroup/vC なので、これ以上作成できることに意味がない、ということと覚えている
    + Q. "How many DHCP pools can be created on the NSX Edge?"
        * 20,000
        * 覚えるしかない?
        * "NSX DHCP service can provide configuration of IP pools, gateways, DNS servers, and search domains."
    + Q. "What is the maximum number of audit logs retained by the NSX Manager?"
        * 1,000,000
        * 覚えるしかない
* デプロイメント
+ Q. "What is the minimum vSphere configuration needed to deploy NSX?"
    * A cluster of ESXi hosts managed by vCenter Server
+ Q. "What is the minimum vSphere 6.0 license edition required to deploy NSX?"
    * 今は、any vSphere edition で動作する。Enterprise plus が必要だったのは昔の話。
    * 「いやいや、vDS必要でしょ」と思うかもしれないですが、そのあたりは、 [VMware NSXには、vSphere Enterprise Plusが必要？それは過去の話です。](http://infratraining.blogspot.jp/2015/07/vmware-nsxenterprise-plus.html) に書かれています。
+ Q. "Which two components are valid minimum prerequisites for installing NSX in a vSphere environment? (Choose two.)"
    * VMware vCenter Server 5.5 or later
    * VMware Tools 8.6 or later
    * ESXi 5.0 or later
+ Q. "What is the packet size of the VXLAN standard test packet when using the Ping test on the logical switches?"
    * 1,550
    * VXLAN 分のオーバーヘッドは 50 byteなので。


### 良く意味がわかっていない

+ Q. "What is the minimum number of vSphere Standard Switches (vSS) that must be configured before deploying VMware NSX for vSphere?"
    * 選択肢は、0, 1, 2, 3 のどれかで、正解は0。
    * 解説は、 "NSX includes logical switches. The NSX logical switch creates logical broadcast domains or segments to which an application or tenant virtual machine can be logically wired." となっていた。
    * いまいち問題の趣旨がわかっていない。答えるとしたら 0だけど、解説を読む限りは、「NSX自体をデプロイするのにportgroupが必要になるけど、それはvDSで作れば良い」とかそういう話ではないっぽい。

## NSX の概要おさらい

おさらいなので、一度でもNSXについて理解したことのある人向け。

### NSX のアーキテクチャ

* Management plane
    * NSX Manager
* Control plane
    * NSX Controller
    * 論理ルータコントロール VM
* Data plane
    * ESXi カーネルモジュール
        * 論理スイッチ
        * 分散ルータ
        * 分散FW
    * Edge

### NSX のコントローラ

* コントローラは必ず3つデプロイする。
* コントロールプレーンとして、4つのテーブルを持つ
    * ARP
    * MAC
    * VTEP
    * ルーティング
* コントローラとESXiホストのカーネルモジュールは、分散FWを除いて、netcpaというUWAを通じて通信する。(VXLAN, 論理ルータなど。)
    * UWAはカーネルモジュールと通信してよしなにする。
    * 分散FWは、直接カーネルモジュールがvsfwdを通じて、NSX Managerと通信する。
* コントローラは、Paxos ベースのアルゴリズムで分散処理している
    * マスターを選出
    * VXLAN, 論理ルータのそれぞれに対して、スライスを作成し、各コントローラに割り当てて処理させる
    * コントローラの追加・削除時には再度スライスの分散が行われる

## NSX の VXLAN

### プロトコル概要
* VXLAN は 24bitのIDを持っていて、VNI という。(つまり、 1677万以上ある)
* VXLAN のオーバーヘッドは、 50byte分ある
    + MTUは少なくとも 1550byteである必要がある
    + IPv6 のことも考えると、推奨は、1600byte以上らしい
    + ジャンボフレームを設定すれば間違いない
* カプセル化後のパケットは、 4789/UDP
* VNI のうち、1NSXでは、10,000までしか利用できない
* VNI のうち、5,000からしか利用できない
* 論理スイッチを作成するとき、レプリケーションモード(マルチキャストモード、ハイブリッドモード、ユニキャストモード)を選択する。それにより、BUMトラフィックのパケットフローが大きく変更される。
    * BUMトラフィックとは、 ブロードキャスト、不明なユニキャスト、マルチキャストのトラフィックのこと

### トランスポートゾーン

* トランスポートゾーンは、VNI用の境界になる
    * Layer 3/VXLAN ネットワークの境界になるという意味
* VXLANオーバーレイのメンバーまたは、VTEPを定義している。
    * 異なるvSphereクラスタのESXiホストを含めることができる
    * 1個のクラスタを複数のトランスポートゾーンに含めることもできる

### VTEP,MTEP,UTEP

* VTEP
    * VXLAN のカプセル化、またはカプセル化の解除を行うエンドポイント
    * vSphereでは、vDS上の VMkernelポートでカプセル化される
    * NSXと連携可能な H/W VTEP も世の中には存在する予定
* VTEPプロキシ : リモートセグメントにある別のVTEPから受け取ったVXLANトラフィックをローカルセグメントに転送するVTEP。MTEP,UTEPがある。

### レプリケーションモード

* それぞれの場合のBUMトラフィックの図が以下のサイトにある
    * [VXLAN simplified - what, why and how ?](http://ccietrip.blogspot.jp/2015/11/vxlan-simply-what-why-and-how.html)
* マルチキャストモード
    * Layer 2でIGMPが有効化されていて、かつ、Layer 3でマルチキャストルーティングが必要
    * ローカルもリモートのどちらのトラフィックもマルチキャストのパケットを投げる
* ハイブリッドモード
    * Layer 2でIGMPが有効化されている必要
    * ローカルではマルチキャストで投げ、リモートにはMTEPへユニキャストパケットを投げる
    * MTEPは受け取ったパケットをローカルセグメントへマルチキャストとして投げる
* ユニキャストモード
    * 特に制限はない
    * ローカルもユニキャストで投げ、リモートにはUTEPにユニキャストパケットを投げる
    * UTEPは受け取ったパケットをローカルセグメントへユニキャストとして投げる
