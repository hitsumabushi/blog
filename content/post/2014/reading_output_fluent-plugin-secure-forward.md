---
title: fluentd-plugin-secure-forward のソースを読んでみる(Output プラグイン編)
date: 2014-12-18T10:03:00+09:00
slug: 1003
categories:
  - blog
tags:
  - Ruby
  - Fluentd
draft: true
---

[昨日の続き]({filename}/diary/2014/reading_input_fluent-plugin-secure-forward.md)で、次はOutput部分の処理を見ようと思います。
Fluentdプラグイン自体の読み方はだいぶわかったので、今日はもう少し詳しいロジックを見ていこうと思います。


## さっそく読む
### initialize

```rb
    def initialize
      super
      require 'socket'
      require 'openssl'
      require 'digest'
      require 'resolve/hostname'
    end
```

必要なライブラリをrequireしています。
こういうのって、クラス定義やファイルに書かずに、initializeでやると嬉しいことがあるんでしょうか。
あまり深く考えてないですが、それほど気にしなくとも良いかな、と思っています。

### configure

```rb
    def configure(conf)
      super
      ...
      @nodes = []
      @servers.each do |server|
        node = Node.new(self, server)
        node.first_session = true
        @nodes.push node
      end
      ...
      @next_node = 0
      @mutex = Mutex.new
      ...
      true
    end
```

``@servers``に何が入っているか考えてみます。例によって、
```rb
    require 'fluent/mixin/config_placeholders'
    ...
    module Fluent
      class SecureForwardOutput < ObjectBufferedOutput
        include Fluent::Mixin::ConfigPlaceholders
        ...
      end
    end
```
という風に書かれているので、super以降は、プレースホルダーが展開されています。そういうわけで、``@servers``には、設定ファイル中のserverディレクティブの設定値が展開された状態で入っています。
server情報を1つずつ、output_nodeとしてインスタンスを作成していき、``@nodes``には、各server情報から作成した、output_nodeを格納しています。
[Mutex](http://docs.ruby-lang.org/ja/2.1.0/class/Mutex.html)を使っているのは、output先が複数あるときに、競合しないようにするためだと思います。

### start

startを見ると、``:node_watcher``を新しいスレッドで実行します。
なので、node_watcherを見てみましょう。

```rb
    def node_watcher
      ...
      loop do
        ...
        (0...nodes_size).each do |i|
          ...
          next if @nodes[i].established? && ! @nodes[i].expired?

          next if reconnectings[i]

          reason = :expired

          unless @nodes[i].established?
            log.warn "dead connection found: #{@nodes[i].host}, reconnecting..."
            reason = :dead
          end

          node = @nodes[i]
          log.debug "reconnecting to node", :host => node.host, :port => node.port, :expire => node.expire, :expired => node.expired?

          renewed = node.dup
          renewed.start

          Thread.pass # to connection thread
          reconnectings[i] = { :conn => renewed, :at => Time.now, :reason => reason }
        end
        ...
```
各output_nodeは、
- established
- expired
- reconnecting




### stop
