Consul 使ってみる
###########################

:date: 2014/11/01 02:43:20
:tags: consul, provisioning, cluster
:category: blog

Consul とは
---------------

特徴
^^^^^^^
* Service Discovery

   * Consulのクライアントは、"api"や"mysql"といった与えられた名前を持つサービスを提供
   * 他のクライアントは、Consulを使ってサービスを検出
   * アプリケーションはConsulが検出したサービスを、DNSやHTTP経由で検出

* Health Check

   * 多くのヘルスチェックの提供
   * 実行されているサービスやノード上の情報などと連携
   * この情報を元に、クラスターの状態を監視
   * サービス検出コンポーネントを使って、良くない状態のホストを迂回できる

* Key/Value Store

   * アプリケーションはConsulの階層的なKey/Valueストアを利用できる
   * 動的な設定変更や、フラグを立てたり、色々使える
   * HTTP APIで簡単に使える

* Multi Datacenter

   * リージョンのことは気にしなくても、Consulが上手いことやる
   * (複数のgpssipプールを持っている云々書いているので、LANとWANで変えているのだと思う)

ステータスの確認のためには、謎のキレイなWebUIもある。

個人的に良いと思っているところ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* DNSインターフェースでホストのIPを取得できるので、クラスター用のDNSサーバーのメンテナンスがいらないのが嬉しい
* ホストの情報が散らばらずに、各サーバーで書かれている。それでいて、問い合わせは分散させられるのが嬉しい。
* 一貫性は正義

登場するサーバー
^^^^^^^^^^^^^^^^^^^^^^^^^
* Agent

   * Server or Client
   * HTTP, DNS, RPCのインターフェースを持ちうるやつ。
     (実際に、持つかどうかは、起動時のclientオプションで決まる)

* Server

   * クラスタ状況の管理
   * クライアントからのRPCへの応答
   * WAN側gossip, リモートデータセンターのリーダーへクエリ
   * クラスタ内ではそれほど多くなくて良いはず

* Client

   * サーバーにRPCを送ってアピール
   * (gossipプールへの参加に関することを除いて、)割とステートレス
   * 通信料もそんなに多くない
   * いくらでもいて良い

インストール
----------------------
バイナリを持ってきて、パス通ってるとこに置く。

http://www.consul.io/downloads.html


起動方法
-----------------------
* Agentの起動

.. code-block:: sh

   # server : serverオプションを指定
   # - clientオプションは、RPC, DNS, HTTPのためのもの
   # - bindオプションは、cluster情報のやりとりに使うっぽい
   # - dcはデータセンター名らしい
   # - nodeはホスト名
   # - bootstrapは最初の1つだけにつける。他は大体joinしとけば良い。
   consul agent -server -bootstrap -client=192.168.2.5 -dc=local \
         -node=con -data-dir=/tmp/consul -bind=192.168.2.5 

   # client
   # - joinオプションで、agentのアドレスを指定。何個か書けるらしい
   consul agent -dc=local -node=consul2 -data-dir=/tmp/consul2 \
         -bind=192.168.39.6 -join=192.168.39.5

* Agentの再起動

Agentの再起動時には、 *SIGHUP* を送れば良い。

使い方
------------

clusterからの情報を取得
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Consulメンバー

.. code-block:: sh

   # 自分の胸に聞くときは、"-rpc-addr"は不要
   consul members
   # クラスタの外にいたりして、誰かに教えてもらうとき
   consul members -rpc-addr=192.168.2.5:8400

* HTTPインターフェース

.. code-block:: sh

   # JSON形式で情報が返る
   curl 192.168.2.5:8500/v1/catalog/nodes

* DNS

.. code-block:: sh

   # 聞く先は適当に。 anyリクエスト投げとけば良いと思う
   # <hostname>.node.consul (データセンターはlocalになる)という形式か、
   # <hostname>.node.<datacenter>.consul という形式で問い合わせ。
   dig @192.168.2.5 -p 8600 con.node.local.consul

Key/Valueストア
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* put

.. code-block:: sh

   curl -X PUT -d 'first object' 192.168.2.5:8500/v1/kv/namespaces/keyname

   # Check-And-Set : atomicなkey変更をするときに使うパラメータ
   # ModifyIndex の値を指定して更新できる。
   # まず、GETしてModifyIndexを見てPUTする、という操作をatomicにできる
   curl -X PUT -d 'first object' 192.168.2.5:8500/v1/kv/namespaces/keyname?cas=97


   
* get

.. code-block:: sh

   curl -s 192.168.2.5:8500/v1/kv/namespaces/keyname
   # => jsonが改行もされず表示されて辛い気持ちになる
   curl -s 192.168.2.5:8500/v1/kv/namespaces/keyname | python -mjson.tool
   # => 見やすくしてくれる
   curl -s 192.168.2.5:8500/v1/kv/namespaces/?recurse
   # => 再帰的に見てくれる
   
   # index=101 : ModifyIndexが101より大きいものが帰ってくるまで聞き続ける
   # wait=5s などすれば、5秒までしか聞かない


もっとConsul
----------------------------

Service, Health Check を定義する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| 定義はjson形式で書く。
| サービスを定義したいサーバーの例えば、/etc/consul.d/以下に

.. code-block:: json

   # /etc/consul.d/mysql.json : サービスを定義
   {"service": {"name": "mysql",  "tags": ["mysql", "db"],  "port": 3306}}

   # /etc/consul.d/ping.json : pingステータスをチェック
   {
   "check": {"name": "ping",  "script": "ping -c1 google.com >/dev/null",  "interval": "30s"}
   }

   # /etc/consul.d/web.json : サービスを定義しつつ、サービスレベルでヘルスチェック
   {"service": {"name": "web",  "tags": ["rails"],  "port": 80, 
   "check": {"script": "curl localhost:80 >/dev/null 2>&1",  "interval": "30s"}}}

とか書いて、起動オプションに、 -config-dir=/etc/consul.d を加える。

Service, Halthの確認
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
他のサーバーから定義されたサービスやステータスを知りたい。

* DNS

| NAME.service.consul or TAG.NAME.service.consul を使う。
| さらに、SRVレコードを見れば、ポートもわかる

.. code-block:: sh

   # Serviceを知る
   dig @127.0.0.1 -p 8600 mysql.service.consul SRV
   dig @127.0.0.1 -p 8600 db.mysql.service.consul SRV

   # Health Checkに失敗してるやつ
   dig @127.0.0.1 -p 8600 web.service.consul

* HTTP

.. code-block:: sh

   # Serviceを知る
   curl -s http://192.168.2.5:8500/v1/catalog/service/mysql

   # Halth Checkに失敗してるやつ
   curl http://localhost:8500/v1/health/state/critical




参考資料
----------------
* `Introduction to Consul <http://www.consul.io/intro/index.html>`_
* `Consul vs. Serf <http://www.consul.io/intro/vs/serf.html>`_ (`Consul vs Serfの日本語訳 <http://pocketstudio.jp/log3/2014/04/19/translation_consul_related_documents/>`_)
* `Serf という Orchestration ツール #immutableinfra <http://www.slideshare.net/sonots/serf-iiconf-20140325>`_

Advanced
^^^^^^^^^^^^^^^^^^^^
* http://www.consul.io/docs/internals/index.html

