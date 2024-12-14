---
title: VDI, DaaS市場を調べてみた
date: 2015-06-07T03:31:00+09:00
slug: '0331'
aliases:
  - 0331.html
categories:
  - blog
tags:
  - VDI
  - DaaS
  - AWS
  - Azure
  - VMware
---

最近、vCloud AirがDaaSを出すというのを聞いて、にわかに自分の中でDaaSに興味が出てきた。
DaaSとかVDIは、必ずActive Directoryの話になるので、気後れしていたのだけど、会社ではWindows使っていることもあって、少しは抵抗もなくなってきたので、良いタイミングだったので、調べてみた。
とは言っても、まずは世間にどんなものがあるかをしらべてみただけ。


## 参考資料
- [http://www.netone.co.jp/report/column/20120302.html](http://www.netone.co.jp/report/column/20120302.html)
- [VSANでの検証](http://www.netone.co.jp/wp-content/uploads/2012/04/7b40e88a83e27031958fd41b697e679d.pdf)
- [アプリケーション仮想化の概説](http://www.dell.com/downloads/jp/solutions/whitepaper/solution/Application_Virtualization_Comparison.pdf)

## 利用シーン
### 世の中の利用シーン
1. オフィス内からの利用
	- [Cisco WAASなどのTCP圧縮・冗長排除・キャッシュ](http://www.cisco.com/web/JP/news/cisco_news_letter/tech/waas2/index.html)
2. 出先での利用
	- オフィス?
	- 映像系の人は?

## VDIまわりとは一体何か?
- オフラインVDI: ユーザーデータのみロードパターンもある
- VDI: VDI, DaaS
- アプリケーション仮想化: アプリケーションごとの配信。thinappとか
### VDIの特徴
1. ユーザーごとにデスクトップを割り当て
2. クライアント集中管理
3. 可用性向上
### 検討ポイント
1. 動画/Flash利用ユーザーへの配慮
2. 回線の悪い状況(帯域が狭い場合 / レイテンシが悪い)のユーザー
3. GPUの利用は?
4. マルチデバイスで利用可能か?
	- Zero Client みたいなものもある
	- Chrome book
## なぜ使うのか、何が課題か
よく書かれているのは、以下の通り。

1. 運用コスト
	- パッチ当て
2. セキュリティ
	- 端末紛失
		+ ユーザーのデータを端末に残さない
3. 災害対策・BCP
	- 安全なDCを使う
4. ワークスタイル変革

## オンプレでやるとすると
### キャパシティプランニング
ブートに必要な領域。さらにメールデータも注意。
個別のプロファイルを持たせている場合は、そのデータストア、フォルダリダイレクトを行う場合、ファイルサーバーに負担がかかる。

1. ストレージ
	- IOPS
		+ 1ユーザーあたりの性能データ取得
			- ユーザー分布を調査
		+ 同時接続数の測定
	- バースト時IOPS
		+ 最大ユーザー数
		+ フラッシュストレージの検討
	- 容量
2. ネットワーク
	- CIFSのパケットのやりとりが非常に多い
3. ファイルサーバー
    - CIFSで死ぬ

### 性能検証
1. ストレージ
	- ストレージシステムコントローラ性能
		+ SPECやSPCのベンチマーク結果
		+ 縮退時のこともあるので、結局N-1~N-2程度での性能
	- ディスクIO性能

## 現状のサービス
### Amazon
- Amazon Workspace
	+ vCPU, mem, storage, office, ...を選択可
	+ $35/month~
	+ 1ユーザー1台
	+ Windows Server 2008R2のみ
	+ ユーザー領域はS3
		- 12hourごとのバックアップ
	+ VDIの動的割り当てみたいなものはない
	+ いつも通りβ版っぽい
		- 毎週日曜日 0:00-4:00までは利用不可
	
- Amazon Workspace Application Manager(Amazon WAM)
    + アプリケーション仮想化
	+ 普通のやつ
	+ ライセンス管理とかできる??
		- 使用頻度が取れる
	+ 割とお高い。$5/user

- Amazon WorkDocs Sync
	+ ドキュメントストアみたいなやつ
### VMware
- Horizon Air
	+ http://www.atmarkit.co.jp/ait/articles/1505/21/news054.html
	+ 4300円/month~ , 50台以上
	+ Desktop DRという安価サービスもある。ただ、復帰が24hour以内はつらい...
		- とはいえ、事前にセットアップしておける、というのは便利なのかも?
		- 700円/month + (起動してる間)300円/日
		- 起動は最低7日なので、起動するには、2100円/月以上
		
### Azure

### 富士通
- V-DaaS
	+ http://fenics.fujitsu.com/outsourcingservice/lcm/workplacelcm/virtualdesktop.html
	+ VMware Horizon DaaSベース
	+ 価格は顧客ID数/構成によって異なるが、参考価格はある
		- 小規模だと1名あたり5000円/month前後~。大規模だと3000円/month強くらいまでいける。
		- 同時接続数での課金ではなさそう?
	+ デフォルトだと1台、420MHz/2GB Mem/40GB disk
	+ 3ヶ月/20ID以上~
	+ いろんなオプションはありそうだし、さすがに富士通って感がある
		- SIベースなのかな?

### 新日鉄ソリューションズ
- $M^3$ DaaS@absonne
	+ http://www.absonne.jp/service/m3daas/menu3.php
	+ 画面転送、仮想デスクトップ型の2タイプ
	+ XenApp, XenDesktopベース
	+ 標準メニューではスペックが低め
		- オプションで増やせそうだけど、価格不明
	+ オプションはたくさん(書いてある): すべて価格不明
		- スナップショット、定期バックアップ
		- ウイルススキャン
		- 2要素認証とか、インターネットGW
		- MDM
		- ストレージサービス
		- ADサービス
	+ 新日鉄という名前が私に、このサービスはSI前提だと囁いている
		- 本当のところ、どんなサービスなんだろうか
		- DaaSの国内シェアNo.1らしいし、利用者の話を聞いてみたい

## まとめ
とりとめもなく、ggったことを書いてみたけど、やはりWindows連携が大事にされているっぽい。
Windowsのことはよくわからないけど、少しオンプレVDIのネットワーク特性については、興味が湧いてきた。
特性として、概ねブートストームと、CIFSの特性の2つで決まりそうだけど、機会があれば実験したい。(機会はたぶんない。)
