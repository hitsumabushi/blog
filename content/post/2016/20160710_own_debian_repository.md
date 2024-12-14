---
title: s3で自前 Debian Package リポジトリを作る
date: 2016-07-10T03:44:00+09:00
slug: '0344'
aliases:
  - 0344.html
categories:
  - blog
tags:
  - debian
  - apt
  - s3
---


## この記事でやること

* aptly の初歩的な使い方
* aptly を使ってs3へ自前リポジトリを公開する。

自前パッケージの作成については、書かないです。


## 自前 Debian Package リポジトリ

なぜ自前のリポジトリが欲しいかというと、個人的には以下の3つくらいかと思います。

* カジュアルにパッチを当てて、サーバに適用したい
* 必要なパッケージをフリーズしたいが全てのサーバーで Pin するのは面倒、などの理由で自分でバージョンをコントロールしたい
* 公式パッケージがない場合に、ビルド済みのものをインストールする形式にしたい

ただし、リポジトリの構成を調べたり、一度手で作ってみるとわかるが、更新がとっても大変です。
そのため、`aptly` や `reprepro` といったリポジトリを管理するためのツールがあります。

## aptly

![aptly](/images/2016/aptly/aptly_log.png)

リポジトリ管理を行うツールで、かなりリポジトリ管理のフローを考慮されたツールになっています。
全く新しくリポジトリを作る場合や、リポジトリのミラーをしたりできます。
特に個人的に便利に使えそうだと思っているのは、スナップショットの機能で、複数のリポジトリからスナップショットを作成できます。
スナップショットを作成して、s3(やs3互換ストレージ)やswiftへアップロードすることができます。

注意点として、リポジトリのミラーをする場合、現状、自分のGPG keyになってしまうようで、ミラーのためにこのツールを使うのは難しいです。ミラーをしたいだけであれば、 rsync した方が良いです。
リポジトリのミラーを resign なしで作成できるようにする機能は作成途中のようです。

また、今回はs3にアップロードする前提ですが、aptly自体は、自前サーバーで公開するためにも利用可能になっています。
その場合にもほとんど同じフローでできます。


## インストール

`sudo apt-get install aptly` すれば良いです。

## 自前のパッケージを含むリポジトリをs3へアップロードする手順

### 事前作業

GPG keyの作成が必要です。

```
gpg --gen-key
```

### アップロードするリポジトリの作成

まずは、空のリポジトリを作成します

```
aptly repo create -distribution=wheezy -component=main <repo_name>
```

次に、パッケージをリポジトリに追加します

```
aptly repo add <repo_name> <deb_packages>
```

現状、どんなパッケージが追加されているかは、 `aptly repo show -with-packages <repo_name>` で確認できます。

### スナップショットの作成

さて、必要なパッケージ追加でき、リポジトリをアップロードする準備ができたら、スナップショットを取得しておきます。
最低限、publishする単位ごとにスナップショットを取っておけば良いと思います。
アップロードするのも、このスナップショットをもとに行います。

```
aptly snapshot create <snapshot_name> from repo <repo_name>
```

スナップショットの一覧は、 `aptly snapshot list` です。 `aptly snapshot show -with-packages <snapshot_name>` とすれば各スナップショットの詳細を確認できます。

スナップショット名としては、サービスのバージョンと連携してパッケージをpublishするのであれば、そのバージョンをsuffixにつけるのが良いと思います。通常の運用時には、タイムスタンプをsuffixにつけましょう。

### aptlyのs3設定


事前にs3のアクセスキーなどを取得している前提です。
以下のように環境変数に設定します。(後述する、 aptly.confに書くこともできます)

```
export AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXX"
export AWS_ACCESS_KEY_ID="YYYYYYYYYYYYYYYYYYYY"
```

次に、 `~/.aptly.conf` にバケットの情報を書きます。

```
{
  "rootDir": "/home/hitsu/.aptly",
  "downloadConcurrency": 4,
  "downloadSpeedLimit": 0,
  "architectures": [],
  "dependencyFollowSuggests": false,
  "dependencyFollowRecommends": false,
  "dependencyFollowAllVariants": false,
  "dependencyFollowSource": false,
  "gpgDisableSign": false,
  "gpgDisableVerify": false,
  "downloadSourcePackages": false,
  "ppaDistributorID": "ubuntu",
  "ppaCodename": "",
  "skipContentsPublishing": false,
  "S3PublishEndpoints": {},
  "SwiftPublishEndpoints": {},
  "S3PublishEndpoints":{
    "<endpoint_name>" : {
      "region": "ap-northeast-1",
      "bucket": "<バケット名>",
      "prefix": "debian",
      "acl": "public-read"
    }
  }
}
```

### スナップショットのアップロード

スナップショットをpublishします。
このコマンドを打つと、s3へ自動でアップロードしてくれます。
s3のWebサイトのホスティングを設定していれば、これでパッケージを公開できたことになります。

```
aptly publish snapshot <snapshot_name> s3:<endpoint_name>:
```

### リポジトリの更新について

基本的には、`aptly repo add` → `aptly snapshot create` で良いのですが、アップロードについては、注意が必要です。

```
aptly publish switch <distribution_name> s3:<endpoint_name>: <new_snapshot_name>
```
