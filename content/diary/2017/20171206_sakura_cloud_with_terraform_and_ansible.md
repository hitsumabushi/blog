Title: さくらのクラウドでN百台を管理するためにterraformとansibleを使っている話
Date: 2017-12-05 17:48
Category: blog
Tags: sakrua,ansible,terraform

[TOC]

---

これは、[さくらインターネット Advent Calendar 2017](https://qiita.com/advent-calendar/2017/sakura) として書いた[記事](https://qiita.com/hitsumabushi/items/e89b763dd4fc41e15136) です。

---

さくらインターネットでは、今年4月からIoTプラットフォームの sakura.io をサービス提供しています。
sakura.io は、さくらのクラウド上で本番・検証環境を構築しており、数百台のサーバーを利用しています。

私はリリース直前にチームに参加し、開発の傍ら運用改善活動をしていました。
その結果としてTerraform を導入し、Terraform (+ Terraform for さくらのクラウド) + Ansible で運用することになりました。
導入までの課題と、どのように導入・利用しているのか、について書きたいと思います。

## 運用の課題

### 検証環境と本番環境で構成に差分があり、それに気づきづらい

mesos+marathon を利用したコンテナ実行環境を使ったマイクロサービスアーキテクチャになっていて、それ以外にも、redis, memcached, メッセージキューなどいろいろなコンポーネントがあります。
そのため、個別の開発者がクリーンな環境を気軽に用意しづらいです。


インフラの構成を変更したいと思ったとき、個別の開発者がクリーンな環境を個別に作るのは手間がかかってしまうため、直接検証環境でテストしがちです。その際に、行われた変更がそのまま残ってしまい、本番環境との差が残ってしまっているケースがありました。

### Ansible Playbook の内容と現実に差分がある

もともとOS内の設定はansibleで管理していたのですが、対象ホストの増加、ansible playbookの肥大化に伴い、実行時間が増えてしまいました。
それに伴い、`--limit`,  `--tags` をつけて部分的に実行するようになり、playbook と差分が散見されるようになりました。

## 方針

ansible は全部実行しろ、などとルールを作ることは簡単なのですが、上記に書いたとおり、心理的なハードルによって発生している問題だと思いました。そこでルール化することはエンジニアリングの敗北という感じがしたので、差分がわかるように構成管理することと、差分を定期的にチェックして通知することに集中することにしました。

構成管理として、OS内の部分はansibleを利用していたためそのまま利用し、インフラの構成管理としては、ちょうど [Terraform for さくらのクラウド](https://sacloud.github.io/terraform-provider-sakuracloud/) もあったため、terraformを利用することにしました。

差分の検知としては、terraform plan, ansible check mode を定期的に実行することにしました。

## terraform 導入のために

### terraform のフォルダ構成

[他のクラウドでのベストプラクティス](https://github.com/hashicorp/best-practices/tree/master/terraform) を参考に、フォルダ構成は以下のようにしています。
terraform plan, apply などする場合には、 `pod-xxx` ディレクトリ配下で実行します。

```
.
├── module
│   └── sakuracloud
│       ├── compute
│       │   ├── compute.tf          // compute のエントリーポイント。各roleのモジュールへ変数を渡す
│       │   ├── role-hoge           // role ごとに作成
│       │   │   └── role-hoge.tf    // util の base-wrapperへ変数を渡す。role固有の変数変換はここでやる
│       │   └── util                // 他のroleから読まれる
│       │       ├── base-wrapper    // instance と service-dns を呼ぶためのやつ。他のroleからはこいつを見る
│       │       ├── instance        // 個別のサーバーの、サーバー/ディスク/DNSレコードの作成
│       │       └── service-dns     // roleごとに、DNSレコードがある場合(VIPに紐づくレコードなど)
│       ├── dns                     // さくらのクラウドのドメイン/DNSレコードを管理するために利用
│       │   ├── dns.tf
│       │   └── example
│       │       ├── example.tf
│       │       └── output.tf
│       ├── gslb                    // さくらのクラウドのGSLBを管理するために利用
│       │   ├── api
│       │   │   └── api.tf
│       │   └── gslb.tf
│       ├── network                 // さくらのクラウドのスイッチ/ルーターを管理するために利用
│       │   ├── internal
│       │   │   ├── internal.tf
│       │   │   └── output.tf
│       │   ├── network.tf
│       │   └── output.tf
│       └── simple-monitor          // さくらのクラウドのシンプル監視を管理するために利用
│           └── simple_monitor.tf
└── providers
    └── sakuracloud
        └── pod-xxx                 // システム単位ごとに作る
            ├── pod-xxx.tf          // compute.tf, dns.tf, ... などのモジュールごとのエントリーポイントへ変数を渡す
            ├── terraform.tfstate.d // tfstate。env (今で言うworkspace) で本番と検証環境をわけてる。
            │   ├── dev
            │   └── ...
            └── terraform.tfvars    // 変数をひたすら書く。具体的な値は全てここに書かれているはず。
```

大体はさくらのクラウドのコンポーネントごとに、moduleを作っているのですが、compute のところは大きく変更しています。
サーバー作成と同時に、ディスクの作成や、DNSレコードの作成を行うためです。

例えば、role-hoge というロールが2台あるとき、tfvar中では以下のような変数を作っています。

```
sakuracloud_dns_foo = {
  dev.zone = "dev.example.com"
  staging.zone = "staging.example.com"
}

sakuracloud_role_hoge = {
  dev.ipaddresses = ["192.168.0.10", "192.168.0.11"]
  dev.server_tags = ["hoge", "develop", "__with_sacloud_inventory", "starred"]
  dev.disk_tags = ["hoge"]
  staging.ipaddresses = ["192.168.1.10", "192.168.1.11"]
  staging.server_tags = ["hoge", "staging", "__with_sacloud_inventory", "starred"]
  staging.disk_tags = ["hoge"]
```

これを使って、dev環境でサーバー作成したとき

* サーバー名をFQDNに一致させる
    * `hoge-01.dev.example.com`, `hoge-02.dev.example.com` 
* DNSレコードも合わせて作成する
    * Aレコードとして `hoge-01.dev.example.com` は192.168.0.10, `hoge-02.dev.example.com` は192.168.0.11 に対応させる
* サーバータグとして、ansibleのroleをつける
    * `hoge`, `develop`, `staging` がansible側で利用しているロール名です
* サーバータグとして、 `__with_sacloud_inventory` をつける
    * 一応、terraform 管理外のリソースを許すためにつけています
* サーバータグとして、 `@group=a` などのグループタグをつける
    * 1つ目のサーバーはa、2つ目はb、...4つ目はd、5つ目はaなどとしています

### 既存リソースをterraformにimport

既存のリソースをインポートします。形式としては、以下のような形式です。

```
terraform import 'module.hoge.module.base-instance.sakuracloud_server.base[0]' _リソースID_
```
注意点としては、tfファイルを書いたあと、terraform planすれば、何をインポートしないといけないかわかるのですが、
その表示では、`module.hoge.base-instance.sakuracloud_server.base[0]` というように、途中にmoduleがない形式で表示されます。 import するには都度moduleを書く必要があります。

また、さくらのクラウドにはリソースIDがないけど、terraform で管理できるものがあります。例えばDNSレコードがそうです。
この場合、リソースIDに当たるものを自分で作成する必要があります。
どのように生成するかは、 terraform for さくらのクラウドのソースを見ればよいのですが、参考までにgolangで生成する例を載せておきます。
https://play.golang.org/p/OvQw6BdxVf

### ansible の dynamic inventory のスクリプト作成

<script src="https://gist.github.com/hitsumabushi/73411a6bcb900a05c027ae0c8a39a9b3.js"></script>

上記のような`sacloud_inventory.py`スクリプトをansibleのリポジトリに実行権限をつけて用意しています。
それにより、 `ansible-playbook -i sacloud_inventory.py ...` とすることで、インベントリファイルを書くことなくansibleを実行できます。

このスクリプトで、さくらのクラウドのAPIを叩くところはすべて、 [usacloud](https://github.com/sacloud/usacloud) におまかせしています。
先程の terraform の例であったように、 `__with_sacloud_inventory` が入っていないものは全部無視し、タグは全てグループ名にすることにしています。
(13-22行目は、[Ansible TowerのOSS版であるAWX](https://github.com/ansible/awx) を試しているために入れています。)

もしかしたら、さくらのクラウドの特殊タグである `@group=a` などは除いた方が使いやすいかもしれませんが、監視側からも見るために現状はすべて入れています。

## ansible 側の準備

`ansible-playbook -i acloud_inventory.py site.yml --check` をしたいのですが、しばしば check modeで実行できていないplaybookや、変更がないのにchangedにしているplaybookがあります。これを直しましょう。
check modeで実行できていない、典型的なものとしては以下のようなものがあります。

### 別のtaskの実行結果を参照している
register を使っているタスクAの結果を参照しているタスクBがある場合、check mode 中でAが実行されないため、タスクBのcheck実行時に変数が参照できないエラーが出ます。
これを防ぐには、register を使っているタスクAに `check_mode: no` をつけることです。
check modeでも本当に実行されるようになるため、例えば、ファイルの存在だけを確認している場合など、副作用がない場合のみ、 `check_mode: no` をつけましょう。

### check modeに対応していない(特にshellモジュール) 
実行する判断を行うようなタスクを作って、その結果次第で、タスクを実行するように書き換えます。
新しく作成したタスクでは、上述の通り副作用がないようにし、 `check_mode: no` をつけましょう。

### 補足: DNSゾーンファイルの更新

今回、check modeで実行可能にするためにplaybookをみなしていると、ansible で更新されていないものとして、template指定されたDNSゾーンファイルがありました。
ゾーンファイルは、シリアルを増やしていく必要があるため、面倒だったのだと思います。

確かに、言われるとめんどくさいような気もしますが、やってみると以下のようにすれば良さそうです。

1. 現在のzone fileを見て、現在の serial を取り出し、registerで変数に入れる
2. template ファイルに、 1.で取ったserialを入れて、差分があるかどうかを確かめる
3. もし、2.で差分があったら serialをインクリメントした上で、template を実行する

実際に書いてみると以下のようになると思います。(NSDを利用した場合の例)

```
server:
    port: 10053
    zonesdir: "/etc/nsd/zones"

{% for zone in dns.zones %}
zone:
    name: "{{ zone }}"
    zonefile: "{{ zone }}"

{% endfor %}
```

```
- block:
  - name: parse serial from zone file
    shell: grep ";Serial" /etc/nsd/zones/{{ item }} | awk '{print $1}'
    with_items: "{{ dns.zones }}"
    register: old_serials
    check_mode: no
    changed_when: no
    tags: nsd
  - name: check whether zone files updated or not
    template: src=zones/{{ item.1 }}.j2 dest=/etc/nsd/zones/{{ item.1 }} owner=root group=root mode=0644
    vars:
      serial: "{{ old_serials.results[item.0].stdout }}"
    with_indexed_items: "{{ dns.zones }}"
    diff: no
    register: zonefiles_changed
    tags: nsd
  - name: update zonefile when changed
    template: src=zones/{{ item.1 }}.j2 dest=/etc/nsd/zones/{{ item.1 }} owner=root group=root mode=0644
    vars:
      serial: "{{ old_serials.results[item.0].stdout|int + 1 }}"
    when: zonefiles_changed.results[item.0].changed
    with_indexed_items: "{{ dns.zones }}"
    notify: reload nsd
    tags: nsd

```

## 定期的な差分チェック

ここまでくれば、あとはcronなりJenkinsで、`terraform plan` と `ansible-playbook -i sacloud_inventory.py site.yml --check` を定期的に走らせて、差分があったらslackなりに通知すればオッケーです。
Jenkinsからapplyするようにしておけば、より良いと思います。


## 感想と今後に向けて

ここではインフラのデプロイをどのように改善してきたのかを書きました。
usacloud や Terraform for さくらのクラウドがあるおかげで、規模が大きくなっても楽に管理できている実感があります。
実際、雑に自前スクリプトを書いていたものも捨てていっているところです。


この記事で書いたようにインフラの整合性を確かめることができるようになったので、今後としては、

* (ansibleの実行を [AWX](https://github.com/ansible/awx) で行う(だいたいできた) )
* インフラ/アプリケーションのCDを行うための監視改善。特に node/service discovery改善
* アプリケーションのCD
* terraform, ansible の自動適用
などを目標に改善活動を行っていく予定です。

