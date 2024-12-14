---
title: Fluentd Pluginを作成するときのメモ
date: 2014-12-19T11:11:00+09:00
slug: '1111'
categories:
  - blog
tags:
  - Fluentd
  - Ruby
draft: true
renderer.unsafe: true
---


## 資料
- [Fluentd - Writing plugins](http://docs.fluentd.org/articles/plugin-development#writing-input-plugins)
- [fluentdのためのプラグインをイチから書く手順(bundler版) - tagomorisのメモ置き場](http://d.hatena.ne.jp/tagomoris/20120221/1329815126)
- [fluentdプラグイン講座](http://toyama0919.bitbucket.org/fluentd_plugin_how_to.html#/37)

### 参考にしたプラグイン
0. [fluentd/in\_tail.rb at master · fluent/fluentd](https://github.com/fluent/fluentd/blob/master/lib/fluent/plugin/in_tail.rb)
1. [fluentd-plugin-secure-forward](https://github.com/tagomoris/fluent-plugin-secure-forward)
2. [fluentd-plugin-dstat](https://github.com/shun0102/fluent-plugin-dstat)

## 作るもの
設定された文字列を設定ファイルに設定された時間感覚で、outputする。
設定ファイルのイメージは以下。

<pre>
  &lt;source&gt;
    type practice
    loopstr "foobar"
  &lt;/source&gt;
</pre>

## 準備

0. (gemにするとき、)``bundle gem fluent-plugin-hogehoge`` でgemを作成。
    gemにしなくても、fluentdのplugins以下に直接おけば使える。
1. 実際のfluentdで実験できるように、fluentdをインストールして用意しておく。
    手元でvagrantやdockerを上げておくと便利。
