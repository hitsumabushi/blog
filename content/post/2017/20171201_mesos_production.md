---
title: Mesos の sandbox のログローテーションをする
date: 2017-12-01T20:01:00+09:00
slug: '2001'
categories:
  - blog
tags:
  - mesos
  - docker
---


### 結論

* http://mesos.apache.org/documentation/latest/logging/#logrotatecontainerlogger
* `LogrotateContainerLogger` を使って、 module parameter を設定する

### 概要

Mesos + Marathon 環境でdockerを動かしている。
基本的にコンテナのログは fluentd で飛ばしているのだけど、日に日に mesos slave のディスク容量が圧迫されていた。
調べてみると、 `/var/lib/mesos-slave/slaves/` 以下にあるフォルダのうち、sandbox のログが肥大化していた。
sandbox には stdout, stderr があって、それぞれコンテナのstdout, stderrを記録しているファイルで、mesosからファイルとして取得することができる。
長期的なものは fluentd で飛ばしているので問題ないため、障害時や直近の確認のために sandbox を使うことにして、
短期間でのログローテーションを行うことにした。

### 設定方法

#### LogrotateContainerLogger の利用が可能か調べる

共有オブジェクト `/usr/lib/liblogrotate_container_logger.so` にあることを確認する。
パスが違っても良いが、その場合は以下で出てくるパスも変更する。

#### モジュールの設定ファイルを書く

`/etc/mesos_slave_modules.json` として以下を書く。
```
{
  "libraries": [{
    "file": "/usr/lib/liblogrotate_container_logger.so",
    "modules": [{
      "name": "org_apache_mesos_LogrotateContainerLogger"
      # パラメータを指定するときはここに書く
    }]
  }]
}
```

#### モジュールの有効化

`/etc/mesos-slave/modules` として、以下が書かれたファイルを置く。
```
file:///etc/mesos-slave-modules.json
```

`/etc/mesos-slave/container_logger` として、以下が書かれたファイルを置く。
```
org_apache_mesos_LogrotateContainerLogger
```

#### mesos-slave の起動
mesos-slave を起動する。

#### 動作確認

sandbox を見ると、 stdout.logrotate.conf, stderr.logrotate.conf が出来ている。

![](/images/2017/mesos/mesos_sandbox.png)


ファイルの中身は
```
/path/to/stdout/ {
## logrotate オプション: パラメータで指定してない場合は size 10481664 くらいしかない
}
```
となっている。
