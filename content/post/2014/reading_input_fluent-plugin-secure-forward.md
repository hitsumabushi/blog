---
title: fluentd-plugin-secure-forward のソースを読んでみる(Input プラグイン編)
date: 2014-12-17T23:45:00+09:00
slug: '2345'
markup.goldmark.renderer.unsafe: true
categories:
  - blog
tags:
  - Ruby
  - Fluentd
---

本当は全部読もうと思っていたけど、想像以上に疲れたので、Inputだけにしました。
ただ、整理されているコードなので、Ruby知らなくても読みやすいのは読みやすいと思います。


## 基本情報

1. lib/fluent/plugin/{TYPE}\_{NAME}.rb 以下がプラグインの本体。

    - TYPE : in, out, buf,... etc
    - NAME : プラグインの名前

2. pluginを書く時のお約束

    - Input(Output)プラグインは、module Fluentd内でInput(Output)プラグインを継承してクラスを定義する
    - 設定ファイル中で ``type hoge`` と書きたいなら、``Fluent::Plugin.register_input('hoge', self)`` をクラス定義中に書く
    - ``config_param`` を使うと、インスタンス変数が宣言できる。(実装はまだ読めていない)

3. Fluentdの起動順序 : See [docs.fluentd.org - plugin-development](http://docs.fluentd.org/articles/plugin-development)

    1. Fluent::Supervisor#run\_configure

        1. require
        2. new
        3. configure(conf)

    2. Fluent::Supervisor#run\_engine

        1. start
        2. shutdown

## fluentd-plugin-secure-forward を読み始める

### 準備
何はともあれ、クローンしてきます。

```bash
$ git clone https://github.com/tagomoris/fluent-plugin-secure-forward.git
$ cd fluent-plugin-secure-forward
```

さて、ライブラリの本体は、以下の通りです。

```bash
$ ls lib/fluent/plugin/
in_secure_forward.rb   input_session.rb       openssl_util.rb        out_secure_forward.rb  output_node.rb
```

これを見ると、

- in_secure_forward.rb
- out_secure_forward.rb

があるので、このプラグインは、 input, outputについてプラグインを作っているようです。

### in\_secure\_forward を読む

#### require & new
さっそく中を見てみます。

```rb
require 'fluent/mixin/config_placeholders'
```
これは、[github.com/tagomoris/fluent-mixin-config-placeholders](https://github.com/tagomoris/fluent-mixin-config-placeholders/blob/master/lib/fluent/mixin/config_placeholders.rb)を読んでいます。
動作については、[http://d.hatena.ne.jp/tagomoris/20120820/1345455837](http://d.hatena.ne.jp/tagomoris/20120820/1345455837)に書いてありますが、fluentdの設定ファイル中のプレースホルダ(${...}みたいなの)を展開した状態で、変数に格納してくれるものらしいです。

secure\_forwardを使うときには、 ``self_hostname`` で自分のホスト名を宣言しますが、その時にhostnameコマンドの結果で定義したいのが人情というものなので、その時に使われていそうです。
とりあえず、設定ファイル中の値を参照できることとして(configureメソッドの``super``が呼ばれてから参照できます)、次に進みます。

```rb
module Fluent
  class SecureForwardInput < Input
  end
end
```
これはお約束みたいなやつで、Inputプラグインは、Fluentモジュールの、Inputを継承したクラスとして定義するようです。中身は後で定義されています。

先に進みます。


```rb
require_relative 'input_session'
```
これは暗号化するためのセッションを扱うものなので、後で考えます。

```rb
module Fluent
  class SecureForwardInput < Input
    DEFAULT_SECURE_LISTEN_PORT = 24284

    Fluent::Plugin.register_input('secure_forward', self)

    config_param :self_hostname, :string
    include Fluent::Mixin::ConfigPlaceholders
    ...
```
ここで大事そうなのは、 ``Fluent::Plugin.register_input('secure_forward', self)``です。
これを書いておくと、fluentd.conf(のinputセクション)で ``type secure_forward`` と書いたとき、このプラグインを使います。

```rb
    # Define `log` method for v0.10.42 or earlier
    unless method_defined?(:log)
      define_method("log") { $log }
    end
```

昔はlogを出すときに$logと書いていたけども、今はlogと書く、という差を吸収するための設定みたいです。

#### configure

```rb
    def configure(conf)
      super
      ...
      @clients.each do |client|
        ...
        @nodes.push({
            address: source_addr,
            shared_key: (client.shared_key || @shared_key),
            users: (client.users ? client.users.split(',') : nil)
          })
      end

      @generate_cert_common_name ||= @self_hostname
      self.certificate
      ...
    end
```

最初の superで、fluent/mixin/config\_placeholders を使って、hostnameのプレースホルダーを展開した値を参照できるようになりました。次に、``@clients`` になにが入ってるかといえば、
```rb
    config_section :client, param_name: :clients do
      config_param :host, :string, default: nil
      config_param :network, :string, default: nil
      config_param :shared_key, :string, default: nil
      config_param :users, :string, default: nil # comma separated username list
    end
```
というのがあるので、設定ファイル中 &lt;client&gt;セクションで定義している中身が入っていることになります。
source_addrというのは、クライアントのアドレス、またはネットワークアドレスで、shared\_keyとuserと一緒にpushしています。

``self.certificate``というのを見てみると、@certと@keyが宣言されていないとき、証明書とキーを生成して、@cert, @keyとして定義するものです。このときコモンネームは、``@generate_cert_common_name ||= @self_hostname``から決まっているので、指定がないならホスト名になります。


#### start & shutdown
さて、configureは読んだので、実行時の挙動を調べます。

```rb
    def start
      super
      OpenSSL::Random.seed(File.read("/dev/urandom", 16))
      @sessions = []
      @sock = nil
      @listener = Thread.new(&method(:run))
    end

    def shutdown
      @listener.kill
      @listener.join
      @sessions.each{ |s| s.shutdown }
      @sock.close
    end
```

特に、変なところはないですが、``@listener, @session`` の中身が気になるところです。早速 runの中身を見てみましょう。

```rb
    def run # sslsocket server thread
      log.trace "setup for ssl sessions"
      cert, key = self.certificate
      ctx = OpenSSL::SSL::SSLContext.new
      ctx.cert = cert
      ctx.key = key

      log.trace "start to listen", :bind => @bind, :port => @port
      server = TCPServer.new(@bind, @port)
      log.trace "starting SSL server", :bind => @bind, :port => @port
      @sock = OpenSSL::SSL::SSLServer.new(server, ctx)
      @sock.start_immediately = false
      begin
        log.trace "accepting sessions"
        loop do
          while socket = @sock.accept
            log.trace "accept tcp connection (ssl session not established yet)"
            @sessions.push Session.new(self, socket)

            # cleanup closed session instance
            @sessions.delete_if(&:closed?)
            log.trace "session instances:", :all => @sessions.size, :closed => @sessions.select(&:closed?).size
          end
        end
      rescue OpenSSL::SSL::SSLError => e
        raise unless e.message.start_with?('SSL_accept SYSCALL') # signal trap on accept
      end
    end
```
あまりOpenSSL:SSL::SSLserverについて調べていないですが、パッと見、

1. 設定されている証明書, キーでSSLサーバーを立てて、loopで待ち続ける
2. テキトーなポート,バインドでリッスンする
3. TCPコネクションが確立されるごとに @sessions に格納していく (``@sock.start_immediately = false``としているので、[SSLはまだハンドシェイクできてない](http://docs.ruby-lang.org/ja/2.1.0/method/OpenSSL=3a=3aSSL=3a=3aSSLServer/i/accept.html))
4. セッションが切れるたびに、@sessionsから削除する

という動作みたいです。特に3.について、なぜこの実装なのかはわかっていないです。
あと、ここで ``@sessions.push Session.new(self, socket)``という部分がありますが、ここのSessionは、input_session.rb で定義されているものです。
こっちの方がこのプラグインの肝な感じですが、Fluentdのプラグインの作り方とはあまり関係ないので、見ないことにします。(最初にping pongをやって、それが終わってから、ソケットを読みにいってはon_messageを呼ぶ、みたいなことをしているみたいです)

とりあえず、以上でざっくりと Inputプラグインの中身がわかりました。

## まとめ
Inputプラグインの場合は、

1. configure(config)
2. start
3. stop

に集中して読み始めるとわかりやすいと思いました。
その他は割と雑多なので、困った時に読めば良さそうです。

## 追記(2014-12-18)

<blockquote class="twitter-tweet" lang="en"><p><a href="https://twitter.com/_hitsumabushi_">@_hitsumabushi_</a> acceptするのはFluentd in_secure_forwardのメインスレッドだけど SSL handshake は割とコストが高い処理なので、それを input_session 側のスレッドにやらせたい、という理由ですね</p>&mdash; tagomoris (@tagomoris) <a href="https://twitter.com/tagomoris/status/545235797960425472">December 17,  2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
