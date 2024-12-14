---
title: DockerHub で docker build のオプションを設定したい
date: 2016-09-27T14:45:00+09:00
slug: 1445
categories:
  - blog
tags:
  - docker
  - dockerhub
---


## 参考リポジトリ
* https://github.com/hitsumabushi/docker-phpipam

## 目的
* Dockerfile の中で、 ARGを使いたい。
    * LABEL としてビルドした日付や、 VCSのリビジョンを入れたい
    * ソフトウェアのバージョンをARGで指定したい

## やること

1. Dockerfile と同じ場所に、 `hook` ディレクトリを作成する。
2. `hook` ディレクトリ以下に、 `build` というファイルを作成する。
    * `build` には、 build時に実行したいシェルスクリプトを書くと、build 時に実行される。
    * 自分で docker build ... というコマンドを書く

## TIPS

### Dockerfileを別の場所に置く場合

https://github.com/hitsumabushi/docker-phpipam では、 Dockerfile を、`/dockerimages/phpipam/` 以下に置いている。
その場合であっても、 Dockerfileと同じディレクトリに、 `hook` ディレクトリを作成すれば良い。
その上で、 DockerHub の Build Settings の Dockerfile Location にて、 `/dockerimages/phpipam/Dockerfile` とすれば良い。

注意点としては、実際にビルドされるとき、 `/dockerimages/phpipam/` 以下でビルドされることになるのだけど、
上位(例えば、リポジトリルート) のファイルなどはビルド中アクセスできない。
もし必要なファイルがあるのであれば、Dockerfileと同じか、そのサブディレクトリに置く必要がある。

### build 中の環境変数の参考
printenvなどすればわかる。
色々便利な環境変数がセットされていて、例えば、以下のようなものが便利そう。

* `GIT_SHA1`      : revision の sha-1 ハッシュ
* `GIT_MSG`       : commit メッセージ
* `SOURCE_BRANCH` : git branch
* `DOCKER_REPO`   : DockerHubで公開されるときのURL
* `DOCKER_TAG`    : ビルドに成功したときに利用されるタグ (Build Settingsで設定できる。)
* `IMAGE_NAME`    : イメージ名 ( `index.docker.io/hitsumabushi/phpipam:latest` のようになる。)

### Dockerfile のラベルについて

Dockerfile には `LABEL` を追加することでメタ情報をつけておくことができる。
フォーマットに関して指定はないが、以下のようなラベルをつけるのも良さそう。

http://label-schema.org/rc1/

### その他のhook
もし、build の前に何かやりたいなどあれば、 `pre_build` などのhookもある。
その他の hook については、 [thibaultdelor/testAutobuildHooks](https://github.com/thibaultdelor/testAutobuildHooks) が参考になる。

