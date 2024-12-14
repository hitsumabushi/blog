---
title: さくらのクラウドでterraformを利用するメモ
date: 2017-04-25T09:25:00+09:00
slug: '0925'
aliases:
  - 0925.html
categories:
  - blog
tags:
  - sakura
  - terraform
draft: true
---


## 資料

* terraform の公式ページ: https://www.terraform.io/
* さくらのクラウド用terraform providerのドキュメント: https://yamamoto-febc.github.io/terraform-provider-sakuracloud/
* best practice: https://github.com/hashicorp/best-practices

## 確認するシナリオ

1. 新しくサーバー、ルーター、スイッチを作成する
    * 3層構成
    * DNS
2. 既存の3層構成のリソースをimportして
    1. サーバーをスケールアウトしてみる
    2. 別のゾーンに作ってみる

## 困った時は
### terraform で管理してるリソースをコンパネ/APIから直接削除してしまった
terraform state rm ... とかで削除してしまうと良いと思う

### `terraform import sakuracloud_disk.disk_import ...` みたいなのをしたら、terraform planで差分が出る
ディスク修正機能で実現されているものは、すべてAPIが返ってこないので、SSH key や source archive が差分になってしまう。
どうしても設定したい場合には、 直接stateファイルに書くしかない。

