Title: 手で書かれたswagger fileを元にAPIをテストする
Date: 2017-05-15 15:08
Category: blog
Tags: api, swagger
Status: draft

[TOC]

# 背景

テストされていないコードにテストを追加する活動をする。
* サービス開発に参加したのは、リリース2ヶ月前
* コードのメインは、API・バックエンドのコード
* コード自体は、Github Enterprise にホストされている
* リリースに向けて、不足している機能もあるため、開発しつつ改善活動をする
* 既存のコードもかなり大きいので、一から書き換えるのは時間的な制約から難しい

# 課題

機能追加されたり、UI側の要望などでAPIを変更した場合に、全体として追従できない。
ドキュメントが更新されなかったり、CLIが更新されなかったりしている。
何を更新しないといけないか把握できていて、アクションできている人がいない。

# 改善

1. 不整合が起きたことを **テスト** によって把握できるようにする
2. 不整合が起きない/起きにくいようにする

# 活動

0. [X] CI環境の整備
1. [X] 課金情報周りの Unitテストを書く活動
2. [X] 謎の手で書かれたswagger fileを正しいswagger fileにする
3. [X] API周りのテスト活動
4. [ ] インフラリソースを管理できるようにする活動
    * 片っ端から terraform import して、不整合は直す
5. [ ] APIドキュメント生成する活動 ← イマココ

## 活動の詳細

### 0. CI環境の整備

CIするためのビルドサーバーがなかった。
何を始めるにも、自動でビルドできるサーバーが必要なので、
お手軽にJenkinsを立てた。

最近のJenkins は `.Jenkinsfile` ファイルを書くことで、ビルド内容を定義できるため、手で色々やる必要がない。
dockerコンテナを利用してビルドする、簡単な `.Jenkinsfile` の例を書いて、共有しておき、pushやPRのタイミングで自動ビルドできるようにした。

### 1. 課金情報周りの Unitテストを書く活動

リリースまで時間も限られているので、最も優先度の高い部分のテストを書くことにした。
そもそもテストしづらいタイプの大きなメソッドを分割することことから始めて、00% → 80%↑ 程度までテストを書いた。

### 2. 謎の手で書かれたswagger fileを正しいswagger fileにする

謎の手書きswagger fileがあった。
swagger fileとしてパースできるが、APIドキュメントとしては不備があって、invalid だった。
(例えば、401が返る場合のbodyがundocumentedだったり、エラー構造体が定義されていないなど)
まず swagger fileとして正しくすることから始めた。
一旦、これは目で見て確かめて書いていく感じにした。(もちろんソースコードを見ることができるので、ソースコードから補完していく感じ。)

swaggerの仕様的に、どうしても表現できないものは諦めた。
(request bodyに依存して、レスポンスのschemaが変わる場合など。)

# 色々と試行錯誤

## swagger-test を使ってテストケースを書く

オリジナルのままだと headerとかも全部deepequalになってるので、
実稼働しているAPIサーバーに対して叩いたりはできない。

また、x-ampleに具体的な例を突っ込む必要があるので、公開するときに表示できないものを削除したりする必要がありそう。
ただ、最初から swagger-test 使うつもりで準備していれば便利そう。

今回は、ちょっと取り回しが悪そうなので、やめた。

## swaggerfile をパースして json schema としてvalidation

x-examplesにリクエストの具体的なパラメータを突っ込んで、
swagger-parse を使って、リクエスト・レスポンスをJSON Schemaから検証した。
required など書き方が違うものがあり、いろいろな書き方を許容してしまうとまずい印象。

JSON Schemaに詳しくなっている時間が惜しいため、最小限だけ実装してみたけど、
dredd を見つけたので、お蔵入り。


## dredd の検証

```
% dredd init
? Location of the API description document swagger.yml
? Command to start API backend server e.g. (bundle exec rails server)
? URL of tested API endpoint https://api-dev.sakura.io
? Programming language of hooks python
? Do you want to use Apiary test inspector? No
? Dredd is best served with Continuous Integration. Create CircleCI config for Dredd? Yes

Configuration saved to dredd.yml

Install hooks handler and run Dredd test with:

  $ pip install dredd_hooks
  $ dredd
```

```
$ pip install dredd_hooks
```
