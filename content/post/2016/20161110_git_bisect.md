---
title: git bisect でバグ/仕様変更のコミットを探す
date: 2016-11-10T03:52:00+09:00
slug: '0352'
aliases:
  - 0352.html
markup.goldmark.renderer.unsafe: true
categories:
  - blog
tags:
  - git
  - ansible
---


## まとめ
* git bisect が便利
* ansible 2.1.0 -> 2.1.1 で group名に `/` を入れるとうまく動かないケースが存在する
    - [ansible](https://github.com/ansible/ansible) リポジトリでbisect すると対象のコミットは `7287effb5ce241ce645d61e55e981edc73fa382a`
    - group名には `/` を入れないように、 `group_vars` 以下はフラットな構成にしよう

## 遭遇した問題
ansible で構成/コンフィグ管理やプロビジョニングをしているのだけど、
複数のリージョンやゾーンにまたがるシステムのため、うまく設定を見やすくするために、
以下のように `group_vars` 配下にディレクトリ構造を作っていた。

### 再現環境

#### ディレクトリ構成
用途やrole, ノードの場所などで、グルーピングして、`group_vars` 以下のディレクトリを作成する。

```
.
├── group_vars
│   ├── env
│   │   ├── production
│   │   └── staging
│   │       ├── app.yml
│   │      (└── vault-pass.yml ※今回は関係ないが暗号化したい情報。ansible-vault で作成。)
│   ├── region
│   │   └── region-1.yml
│   ├── role
│   │   └── web.yml
│   └── zone
│       └── zone-1.yml
├── inventories
│   └── sample.ini
├── library
├── roles
└── site.yml
```

#### group\_vars

```
$ cat env/staging/app.yml
---

app_name: "sample_app_name"
```

#### inventory
各ノードの状況に応じて、`env/staging` や `region/region-1` などにノードを所属させていた。

```
$ cat inventories/sample.ini
[env/staging]
app_server-1
db_server-1

[region/region-1:children]
zone/zone-1

[zone/zone-1]
app_server-1
db_server-1

[role/web]
app_server-1

[app]
app_server-1 ansible_host=localhost

[db]
db_server-1 ansible_host=example.com
```

#### playbook
```
$ cat site.yml
---

- hosts: app
  gather_facts: no
  tasks:
    - debug: msg="{{ app_name }}"
```

### 問題の再現
ansible `2.1.0.0` だと `app_name` を参照できている。

```
$ ansible --version
ansible 2.1.0.0
...
$ ansible-playbook -i inventories/sample.ini site.yml

PLAY [app] *********************************************************************

TASK [debug] *******************************************************************
ok: [app_server-1] => {
    "msg": "sample_app_name"
    }
...
```

ansible `2.1.1.0` だと `app_name` を参照できず、未定義になっている。
```
$ ansible --version
ansible 2.1.1.0
...
$ ansible-playbook -i inventories/sample.ini site.yml

PLAY [app] *********************************************************************

TASK [debug] *******************************************************************
fatal: [app_server-1]: FAILED! => {"failed": true, "msg": "the field 'args' has an invalid value, which appears to include a variable that is undefined. The error was: 'app_name' is undefined\n\nThe error appears to have been in '/home/hitsu/tmp/blog/site.yml': line 6, column 7, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n  tasks:\n    - debug: msg=\"{{ app_name }}\"\n      ^ here\nWe could be wrong, but this one looks like it might be an issue with\nmissing quotes.  Always quote template expression brackets when they\nstart a value. For instance:\n\n    with_items:\n      - {{ foo }}\n\nShould be written as:\n\n    with_items:\n      - \"{{ foo }}\"\n"}

...
```

## コミット履歴の調査
コードを読むと[この辺](https://github.com/ansible/ansible/blob/devel/lib/ansible/inventory/__init__.py#L797)が怪しいというのはわかるが、コードを順番に読んでいくと時間がかかるので、調査する範囲を絞りたい。
そこで、どのコミットまで正しく動作していて、どのコミットから挙動が変わっているのかを知りたい。
最初、手作業で二分探索していたが、Twitterで mapk0yさんに`git bisect` を教えてもらった。

<blockquote class="twitter-tweet" data-lang="en"><p lang="ja" dir="ltr"><a href="https://twitter.com/_hitsumabushi_">@_hitsumabushi_</a> なんのことか全然わかってないの勘違いしてるかもしれませんが、ちゃんと問題の検出ができるならば git bisect を使えば二分探索で怪しいコミットを見つけることができるはずです。</p>&mdash; mapk0y (@mapk0y) <a href="https://twitter.com/mapk0y/status/796385700371275776">November 9, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

## git bisect での調査
### リポジトリのクローン
```shell
git clone https://github.com/ansible/ansible.git
```
### テストスクリプトの準備
```shell
$ cd ansible
$ cat check.sh
#!/bin/sh

PATH_TO_PLAYBOOK="${HOME}/tmp/sample"
PATH_TO_ANSIBLE="${HOME}/tmp/ansible"

cd "${PATH_TO_ANSIBLE}"
git submodule update --init --recursive
pip uninstall -y ansible; pip install "${PATH_TO_ANSIBLE}"
cd "${PATH_TO_PLAYBOOK}"
ansible-playbook -i inventories/sample.ini site.yml
```

### git bisect の実行(自動)
現在、すでに 2.1.0.0 と 2.1.1.0 の間で動作が変わっていることがわかっている。
タグとしては、 `v2.1.0.0-1` と `v2.1.1.0-1` の間になる。

まずは、 2分探索をどの範囲で実施するか設定して、開始する。
`git bisect start "壊れているコミット" "正しく動作しているコミット"` の順番で指定する。
```shell
$ git bisect start v2.1.1.0-1 v2.1.0.0-1
```

次に、各コミットに対して、 good/bad の判断を行うため、テストスクリプトを指定する。
これで、自動的にテストスクリプトを実行して、2分探索を行ってくれる。
あとは、結果が出るまで待てば良い。
```shell
$ git bisect run ./check.sh
...
7287effb5ce241ce645d61e55e981edc73fa382a is the first bad commit
commit 7287effb5ce241ce645d61e55e981edc73fa382a
...
```
これで、 commitが特定できた。あとは、内容の変更を精査すれば良い。

### 片付け
調査が終わったら、 `git bisect reset` して、終わってしまえば良い。

---

`git bisect` 便利!!


## 参考資料
- [問題のあるコミットを特定する ( git bisect )](http://qiita.com/Shaula/items/1e13808946d8ca8bacbc)
- [github.com/ansible/ansible](https://github.com/ansible/ansible)
- [add\_host module in v2.1.1.0 does not follow paths with forward slash #16881](https://github.com/ansible/ansible/issues/16881)

