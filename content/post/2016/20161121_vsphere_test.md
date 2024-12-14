---
title: VMware Product ごとのtest 方法について
date: 2016-11-21T14:14:00+09:00
slug: '1414'
categories:
  - blog
tags:
  - VMware
  - test
draft: true
---


## 参考にしたリポジトリ

* https://github.com/vmware/pyvmomi
* https://github.com/vmware/govmomi
* https://github.com/vmware/vic

## pyvmomi

[vcrpy](https://pypi.python.org/pypi/vcrpy) を利用している。
元々は、 [vcr](https://github.com/vcr/vcr) というruby製のツールだったもののpython版らしい。
他の言語でも同様のツールはあって、例えば、Go だと [DVR](https://github.com/orchestrate-io/dvr) というのがある。

## govmomi

`vcsim` を使っている。
ただ、vcsim はvSphere 5.5 までしか対応しておらず、6.0以降のためのテストは難しい。
このこと自体は割と前から Issue には挙がっているが、まだ対応はされていない。
https://github.com/vmware/govmomi/issues/358

## vic

自前でテスト用のオブジェクトを作っている。
https://github.com/vmware/vic/tree/master/pkg/vsphere/simulator
vcsim の中で、これを
https://github.com/vmware/vic/blob/master/cmd/vcsim/main.go


