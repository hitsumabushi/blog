---
title: VMware VCP-NV (VCP6-NV) の試験を今週受けるので、試験について調べる
date: 2016-07-05T20:40:00+09:00
slug: 2040
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

## この記事について

1. 書くこと
    - VCP6-NV の試験要項
    - VCP6-NV の受験方法
2. 書かないこと
    - 試験の勉強方法
    - 試験内容

## VCP6-NV について

VCP-NVは、VMwareのNSXを用いた仮想ネットワーク管理についての試験です。
他のVCPと同様に、VCA-NV → VCP-NV → VCAP-NV {Design, Deploy} → VCIX-NV → VCDX-NV というような資格体系です。

![](/images/2016/vmware_vcp/VCP6-NV.png)

上記の図を含め、資格と試験の情報は以下にまとまっています。

[VMware Certified Professional 6 – Network Virtualization (VCP6-NV)](https://mylearn.vmware.com/mgrReg/plan.cfm?plan=64294&ui=www_cert)

### 試験について

まず、今日(2016/07/05) 時点での、試験は、 `2V0-641: VMware Certified Professional 6 - Network Virtualization Exam` です。
以前の試験から、2015/08/30あたりで切り替わっているようです(詳細は調べていません)。
そのため、昔の情報を見る場合には、きちんと現行のVCP-NVになっているのか確かめる必要があります。

### 受講資格について

現在、有効なVCPを持っているかどうかによって異なります。
昔のVCPを持っている人に取っては、あまり馴染みはないですが、現行のVCPの試験には Foundation試験を受けた後、DCVならDCVの試験、NVならNVの試験という風な2段階の試験になっています。
そのため、必要なトレーニングを受講後、試験2つをパスする必要があります。
ただし、現在有効なVCP資格を持っている場合、トレーニングもFoundation試験も免除されるため、NVの試験(`2V0-641: VMware Certified Professional 6 - Network Virtualization Exam`) を受けるだけで問題ありません。

まとめると以下です。

1. 有効なVCPを持っている場合
    1. `2V0-641: VMware Certified Professional 6 - Network Virtualization Exam` を受験し、合格する
2. VCPを保有していない、もしくは失効している場合
    1. 対象のトレーニングの受講
        - NSX: Install, Configure, Manage [V6.0] , [V6.1], [V6.2]
        - NSX for Internetworking Experts Fast Track [V6.0],[V6.1]
        - NSX Troubleshooting & Operations [V6.1] (available as Onsite Training only)
        - NSX: Design & Deploy [V6.2] (available as Onsite Training only)
        - Security Operations for the Software Defined Data Center
    2. vSphere 6 の Foundation試験を受験し、合格する
    3. `2V0-641: VMware Certified Professional 6 - Network Virtualization Exam` を受験し、合格する

### 試験の概要について

このページにまとまっています。
[VMware Certified Professional 6 – Network Virtualization Exam](https://mylearn.vmware.com/mgrReg/plan.cfm?plan=64297&ui=www_cert)

抜粋すると、以下の通りです。

- 試験時間 : 100分
- 問題数 : 85問
- 合格点 : 300点
- 対象のプロダクト : VMware NSX for vSphere v6
- 試験費用 : $225 USD

## まとめ

とりあえず、これから受けるのでまとめてみましたが、以前のVCPの情報よりよくまとまっていて、資格試験としての体裁が整っている印象です。
VMwareの人と話していても、資格試験としてまともなっていると聞くので、受ける価値がありそうです。
(以前のVCPはちょっと・・・という感じの試験内容だった。)

とりあえず、受けたらまた試験について書きます。

## 追記
[VCP6-NV の試験勉強メモを書いた。](/blog/2016/07/05/2121.html)
