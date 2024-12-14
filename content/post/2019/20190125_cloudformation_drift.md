---
title: CloudFormation の不満点
date: 2019-01-25T14:54:00+09:00
slug: '1454'
categories:
  - blog
tags:
  - aws
  - cloudformation
---



以下では「手作業で」というのは、「CloudFormation管理外で」という意味で使う。

## 要点

* CloudFormation は、リソースが何かの理由で手作業で変更されていた場合に安全に操作できない
* Drift 検出は誤検出が多すぎて使いづらい
* Change Set は動いている状態との差分を見ていないので、信用できない

## 経緯

CloudFormation で管理されているリソースすべてについて、新しいタグをつけたくなった。
ただ、各サービスの担当者ごとにある程度自由にオペレーションできるため、手動で変更されていないか、一応調べておこうと思い、
[2018-11 にリリースされたドリフト検出](https://aws.amazon.com/jp/blogs/news/new-cloudformation-drift-detection/) を使って、
手作業で実施された変更点もCloudFormationに取り込みつつ、対応しようとした。


## 期待したこと

* CloudFormation のスタックがたくさんあるため、1つ1つ細かく差分を見て修正することが難しい
* ドリフト検出されたところだけ1つずつ修正していって、Change Setを作りながら現状に合わせたい

## 実際

### ドリフト検出


* サポートされるリソースが少ない
  * [Resources that Support Drift Detection](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift-resource-list.html)
* そもそも誤検出が多い
  * [Detecting Unmanaged Configuration Changes to Stacks and Resources](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html?shortFooter=true#drift-considerations)
  * LBのプロパティなど、配列で定義されるところをデフォルト値で埋められただけで、ドリフトが検出される
  * エッジケースの(とAWSが主張している)誤検出に該当するのか、目で見て考える以外の方法がない

### Change Set

* 実際に動いているシステムとの差分を見ていない
  * 前回の設定とのスタックの差分を見ている
* 手作業で変更されているとChange Setの実行に失敗する(実際には差分がないので)
  * その場合 Update Stack するしかない

例えば、手作業でタグを増やしたとして、翌営業日にCloudFormationに反映したい、と思った場合、
ドリフト検出で誤検知を目でフィルタしつつ(誤検知だと確信が持てるかはわからない)、
CloudFormation のパラメータを書き換えて、Update Stackしないといけない。
(一応、Update Stack 前に Change Set で差分を見て、execute して失敗することを確認したほうが安心感はある。)


## まとめ

手作業の変更をできないようにしておく以外にない。
あるいは、本格的にCloudFormationを利用し始めるまでの間に Terraform に移行する。

(なんでChange SetをRunnning Stateとの比較にしなかったんだろう...)
