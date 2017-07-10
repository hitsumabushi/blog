Title: さくらのクラウドを便利に使うためのツールメモ
Date: 2017-07-10 16:00
Category: blog
Tags: sakura,terraform,peco

[TOC]

# 1. CLIで操作したい

usacloud が今一番良い。
非公式と書かれているが、サポートされている機能、更新頻度、使い勝手、導入のしやすさ、などどれをとっても usacloud を使うべき。

https://sacloud.github.io/usacloud/

## 便利なコマンド

### 〇〇の一覧が欲しい

〇〇 list すれば良い。例えば、以下の通り。
```
# サーバー
usacloud server list
# スイッチ
usacloud switch list
```

### サーバーのメンテナンス情報を知りたい
```
usacloud server maintenance-info
```

### サーバーにSSHしたい
```
usacloud server ssh -l username example_node
```

## peco と usacloud でもっと便利にSSHする

peco ( http://peco.github.io/ ) をインストールする。
以下のようなスクリプトを .zshrc に書く。
<script src="https://gist.github.com/hitsumabushi/5ef85d9ba8afdb667aaf2e9f13dcb0d1.js"></script>

.zshrc を読み込み直して、 `Ctrl + g` を押すと、サーバー名やIPで絞り込みを行って SSH できる。
上記スクリプトではタグ情報を入れていないけど、入れたい場合には、 `usacloud server list --output-type json` などにして、出力を `jq` でフィルタして表示するのが良いと思う。

# 2. terraform 経由で使いたい

usacloud と同じ作者が作っている terraform provider がある。
terraform 公式には入っていないが、インストールも簡単。

https://sacloud.github.io/terraform-provider-sakuracloud/

ただ、既存リソースをインポートして使うにはなかなか大変。
色々 tfstate ファイルを生で書き換える必要がある。
特に、リソースには基本的にIDが必要だけど、さくらのクラウドにIDがないものがある。
例えば、DNSのゾーンにはIDがあるけど、レコードにはIDがない。
これを管理するために、terraform provider 側でIDを生成している。
以下のような形で生成したものをtfstateに書けば良い。
https://play.golang.org/p/rYk3VNLeGN

# 3. ansible で便利に使いたい

TODO
